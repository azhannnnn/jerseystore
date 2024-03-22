"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from app.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',home,name='home'),
    path('products/',products,name='products'),
    path('productdetail/<int:pk>/',productdetail,name='productdetail'),
    path('add_cart/<int:pk>', add_cart, name="add_cart"),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>', remove, name="remove"),
    path('account/',account,name='account'),
    path('checkout/',checkout,name='checkout'),
    path('user/',user,name='user'),
    
    path('registerpage/',registerpage,name='registerpage'),
    path('loginpage/',loginpage,name='loginpage'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),

    path('payment/',payment,name='payment'),
    path('success/',success,name='success'),
    path('myorder/',myorder,name='myorder'),

    #============================================================================================#

   
    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

