from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Customer, Computer, Price, Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from django import template
from django.contrib import messages
from . forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage


register = template.Library()

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{} hours {} min'.format(hours, minutes)


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
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'cyber/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cyber/change_password.html', {'form': form})


@login_required
def userLogout(request):
    logout(request)
    return redirect('userLogin')


def error(request):
    return render(request, 'cyber/error.html')


@login_required
def dashboard(request):
    computerCount = Computer.objects.all().count()
    customerCount = Customer.objects.all().count()
    charges = Price.objects.get(pk=1)
    count = {
        'computerCount' : computerCount,
        'customerCount' : customerCount,
        'price' : charges.price,
    }
    # messages.success(request, f'account created')
    return render(request, 'cyber/dashboard.html', count)


@login_required
def price(request):
    if request.method == "POST":
        temp = request.POST.get('price')
        if temp != "":
            charges = Price.objects.get(pk=1)
            charges.price = int(temp)
            charges.save()
            messages.success(request, f'Charges updated successfully!')
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
        messages.success(request, f'Computer added successfully!')
        return redirect('addComputer')
    return render(request, 'cyber/addComputer.html')


@login_required
def manageComputer(request):
    computers = Computer.objects.all()
    paginator = Paginator(computers, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if computers.count():
        return render(request, 'cyber/manageComputer.html', {'page_obj': page_obj})
    else:
        return render(request, 'cyber/manageComputer.html', {'NC': True})


@login_required
def updateComputer(request, id):
    if request.method == 'POST':
        obj = Computer.objects.get(pk=id)
        obj.computerName = request.POST.get('computerName')
        obj.computerLocation = request.POST.get('computerLocation')
        obj.save()
        messages.success(request, f'Computer updated successfully!')
        return redirect('manageComputer')

    return HttpResponseRedirect('../manageComputer')


@login_required
def deleteComputer(request, id):
    if request.method == 'POST':
        obj = Computer.objects.get(pk=id)
        if obj.availability:
            obj.delete()
            messages.success(request, f'Computer removed successfully!')
            return redirect('manageComputer')
        else:
            messages.error(request, f'Computer is in Use. Unable to remove computer!')
            return redirect('manageComputer')
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
        computerUsed = f'{computer.computerName}, {computer.computerLocation}'
        computer.availability = False
        computer.save()
        obj = Customer(customerName=name, customerAddress=address, customerPhoneNumber=ph, customerEmail=email, computerChoice=computerId, computerUsedName=computerUsed, customerIdProof=id)
        obj.save()
        messages.success(request, f'Customer added successfully!')
        return redirect('addCustomer')
     
    computers = Computer.objects.all()
    return render(request, 'cyber/addCustomer.html', {'computers':computers})


@login_required
def checkout(request):
    customers = Customer.objects.all()
    return render(request, 'cyber/checkout.html', {'customers': customers} )


@login_required
def checkoutCustomer(request, id):
    try:
        customer = Customer.objects.get(pk=id)
        charges = Price.objects.get(pk=1)
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

    except:
        return redirect('error')  
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
        messages.success(request, f'Customer checkout successfull!')

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
def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        if query:
            allcus = Customer.objects.filter(customerName__icontains=query)
            paginator = Paginator(allcus, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            params = {'page_obj': page_obj}
            if allcus.count():
                return render(request,'cyber/search.html', params)
            else:
                return render(request, 'cyber/search.html', {'NRF': True})
    return render(request, 'cyber/search.html', {'bool':True})


@login_required
def contactUs(request):
    return render(request, 'cyber/contactUs.html')


@login_required
def about(request):
    return render(request, 'cyber/about.html')