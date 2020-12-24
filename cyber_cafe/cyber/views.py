from django.shortcuts import render, redirect
from . models import Customer, Computer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
def allCustomers(request):
    customers = Customer.objects.all()
    return render(request, 'cyber/allCustomers.html', {'customers': customers})

@login_required
def demo(request):
    return render(request, 'cyber/demo.html')

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
    return render(request, 'cyber/manageComputer.html', {'computers': computers})

@login_required
def editComputer(request):
    pass

@login_required
def deleteComputer(request):
    pass

@login_required
def addCustomer(request):
    if request.method == 'POST':
        name = request.POST.get('name',)
        address = request.POST.get('address')
        ph = request.POST.get('ph')
        email = request.POST.get('email')
        id = request.POST.get('id')
        obj = Customer(customerName=name, customerAddress=address, customerPhoneNumber=ph, customerEmail=email, customerIdProof=id)
        obj.save()
    return render(request, 'cyber/addCustomer.html')

@login_required
def checkoutCustomer(request):
    pass

@login_required
def about(request):
    pass