from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.userLogin, name='userLogin'),
    path('userLogout', views.userLogout, name='userLogout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/computers', views.computers, name='computers'),
    path('dashboard/customers', views.allCustomers, name='allCustomers'),
    path('dashboard/demo', views.demo, name='demo'),
    path('dashboard/addComputer', views.addComputer, name='addComputer'),
    path('dashboard/manageComputer', views.manageComputer, name='manageComputer'),
    path('dashboard/addCustomer', views.addCustomer, name='addCustomer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)