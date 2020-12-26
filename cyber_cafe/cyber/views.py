from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from . models import Customer, Computer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator

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
    count = {
        'computerCount' : computerCount,
        'customerCount' : customerCount
    }
    return render(request, 'cyber/dashboard.html', count)

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
        # return HttpResponseRedirect('../manageComputer')
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
    return render(request, 'cyber/checkoutCustomer.html', {'customer' : customer})


    # customer.checkOutTime = datetime.now()
    # customer.checkInStatus = False
    # computerAlloted = customer.computerChoice

    # computer = Computer.objects.get(pk=computerAlloted)
    # computer.availability = True
    # computer.save()

    # timeDifference = customer.checkOutTime-customer.checkInTime
    # minutes = timeDifference.total_seconds() / 60
    # hours = minutes / 60
    # customer.duration = timeDifference
    # print(customer.duration)

    # customer.save()
    # print(customer.checkInTime)

    # print(f"Difference = {timeDifference}")
    # print(f"Difference in Minutes = {int(minutes) - int(hours)*60}")
    # print(f"Difference in Hours = {int(hours)}")

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