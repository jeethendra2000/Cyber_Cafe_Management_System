from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('demo/', views.demo, name='demo'),
    path('', views.userLogin, name='userLogin'),
    path('userLogout', views.userLogout, name='userLogout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/price', views.price, name='price'),
    path('dashboard/computers', views.computers, name='computers'),
    path('dashboard/addComputer', views.addComputer, name='addComputer'),
    path('dashboard/updateComputer/<str:id>', views.updateComputer, name='updateComputer'),
    path('dashboard/deleteComputer/<str:id>', views.deleteComputer, name='deleteComputer'),
    path('dashboard/manageComputer', views.manageComputer, name='manageComputer'),
    path('dashboard/addCustomer', views.addCustomer, name='addCustomer'),
    path('dashboard/checkout', views.checkout, name='checkout'),
    path('dashboard/checkoutCustomer/<str:id>', views.checkoutCustomer, name='checkoutCustomer'),
    path('dashboard/checkoutConfirm/<str:id>', views.checkoutConfirm, name='checkoutConfirm'),
    path('dashboard/allCustomer', views.allCustomer, name='allCustomer'),
    path('dashboard/customerBill/<str:id>', views.customerBill, name='customerBill'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)