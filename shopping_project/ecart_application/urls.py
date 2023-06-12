from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from .views import *

urlpatterns = [
    
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('cart/',add_to_cart.as_view(),name='add-to-cart'),
    path('items/',items_list.as_view(),name='items-list'),
    
]
    
