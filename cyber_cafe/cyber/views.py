from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Customer, Computer, Price
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from django import template

register = template.Library()

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{} hours {} min'.format(hours, minutes)


def demo(request):
    c = Customer.objects.all()
    paginator = Paginator(c, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cyber/demo.html', {'page_obj': page_obj})

# Create your views here.
def userLogin(request):
    adminId = request.POST.get('AdminId')
    passwd = request.POST.get('AdminPasswd')
    user = authenticate(request, username = adminId, password = passwd)
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'cyber/login.html')

@login_required
def userLogout(request):
    logout(request)
    return redirect('userLogin')



@login_required
def dashboard(request):
    computerCount = Computer.objects.all().count()
    customerCount = Customer.objects.all().count()
    charges = Price.objects.get(pk=request.user.id)
    count = {
        'computerCount' : computerCount,
        'customerCount' : customerCount,
        'price' : charges.price,
    }
    return render(request, 'cyber/dashboard.html', count)

@login_required
def price(request):
    if request.method == "POST":
        temp = request.POST.get('price')
        if temp != "":
            charges = Price.objects.get(pk=request.user.id)
            charges.price = int(temp)
            charges.save()
    return redirect('dashboard')


@login_required
def computers(request):
    computers = Computer.objects.all()
    return render(request, 'cyber/computersList.html', {'computers': computers})


@login_required
def addComputer(request):
    if request.method == 'POST':
        computerName = request.POST.get('computerName')
        computerLocation = request.POST.get('computerLocation')
        obj = Computer(computerName=computerName, computerLocation=computerLocation)
        obj.save()
    return render(request, 'cyber/addComputer.html')

@login_required
def manageComputer(request):
    computers = Computer.objects.all()
    paginator = Paginator(computers, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cyber/manageComputer.html', {'page_obj': page_obj})

@login_required
def updateComputer(request, id):
    if request.method == 'POST':
        obj = Computer.objects.get(pk=id)
        obj.computerName = request.POST.get('computerName')
        obj.computerLocation = request.POST.get('computerLocation')
        obj.save()
        return redirect('manageComputer')

    return HttpResponseRedirect('../manageComputer')

@login_required
def deleteComputer(request, id):
    if request.method == 'POST':
        obj = Computer.objects.get(pk=id)
        obj.delete()
        return HttpResponseRedirect('../manageComputer')
    return HttpResponseRedirect('../manageComputer')

@login_required
def addCustomer(request):
    if request.method == 'POST':
        name = request.POST.get('name',)
        address = request.POST.get('address')
        ph = request.POST.get('ph')
        email = request.POST.get('email')
        computerId = request.POST.get('computer')
        id = request.POST.get('id')
        computer = Computer.objects.get(id=computerId)
        computer.availability = False
        computer.save()
        obj = Customer(customerName=name, customerAddress=address, customerPhoneNumber=ph, customerEmail=email, computerChoice=computerId, customerIdProof=id)
        obj.save()

    computers = Computer.objects.all()
    return render(request, 'cyber/addCustomer.html', {'computers':computers})


@login_required
def checkout(request):
    customers = Customer.objects.all()
    return render(request, 'cyber/checkout.html', {'customers': customers} )


@login_required
def checkoutCustomer(request, id):
    customer = Customer.objects.get(pk=id)
    charges = Price.objects.get(pk=request.user.id)
    computerAlloted = customer.computerChoice
    computer = Computer.objects.get(pk=computerAlloted)

    if not customer.checkOutStatus:
        customer.computerUsedName = f'{computer.computerName}, {computer.computerLocation}'
        customer.checkOutTime = datetime.now()
        timeDifference = customer.checkOutTime-customer.checkInTime
        customer.duration = duration(timeDifference)
        customer.charge = (((int(timeDifference.total_seconds()) // 60) // 30) + 1) * charges.price
        customer.save()

    return render(request, 'cyber/checkoutCustomer.html', {'customer' : customer})

@login_required
def checkoutConfirm(request, id):
    if request.method == 'POST':
        remark = request.POST.get('remark')
        customer = Customer.objects.get(pk=id)
        if remark != "":
            customer.remarks = remark

        computerAlloted = customer.computerChoice
        computer = Computer.objects.get(pk=computerAlloted)
        computer.availability = True
        computer.save()

        customer.checkOutStatus = True
        customer.checkInStatus = False
        customer.save()

    return redirect('checkout')



@login_required
def allCustomer(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cyber/allCustomer.html', {'page_obj': page_obj} )


@login_required
def customerBill(request, id):
    customer= Customer.objects.get(pk=id)
    return render(request, 'cyber/customerBill.html', {'customer': customer} )

@login_required
def about(request):
    pass
