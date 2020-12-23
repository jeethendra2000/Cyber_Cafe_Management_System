from django.shortcuts import render, redirect
from . models import Customer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def userLogin(request):
    adminId = request.POST.get('AdminId')
    passwd = request.POST.get('AdminPasswd')
    user = authenticate(request, username = adminId, password = passwd)
    print(f'user = {user}')
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'cyber/login.html')

@login_required
def dashboard(request):
    return render(request, 'cyber/dashboard.html')

@login_required
def computers(request):
    return render(request, 'cyber/computersList.html')

@login_required
def allCustomers(request):
    return render(request, 'cyber/allCustomers.html')

@login_required
def demo(request):
    return render(request, 'cyber/demo.html')

@login_required
def addComputer(request):
    return render(request, 'cyber/addComputer.html')

@login_required
def manageComputer(request):
    pass

@login_required
def editComputer(request):
    pass

@login_required
def deleteComputer(request):
    pass

@login_required
def addCustomer(request):
    name = request.POST.get('name', False)
    address = request.POST.get('address', False)
    ph = request.POST.get('ph', False)
    email = request.POST.get('email', False)
    id = request.POST.get('id', False)
    obj = Customer(customerName=name, customerAddress=address, customerPhoneNumber=ph, customerEmail=email, customerIdProof=id)
    obj.save()
    return render(request, 'cyber/addCustomer.html', {"name": name})

@login_required
def checkoutCustomer(request):
    pass

@login_required
def about(request):
    pass