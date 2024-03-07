from django.urls import path,include

from .views import *

urlpatterns = [
    
    path('',home,name='home'),
    path('products/',products,name='products'),
    path('productdetail/<int:pk>/',productdetail,name='productdetail'),
    path('add_cart/<int:pk>', add_cart, name="add_cart"),
    path('cart/',cart,name='cart'),
    path('remove/<int:pk>', remove, name="remove"),
    path('account/',account,name='account'),
    path('checkout/',checkout,name='checkout'),
    
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
]