from . import views
from django.urls import path
from accounts.views import *


urlpatterns = [
    # landing page
    path('trading', views.Trading_menu.as_view(), name = 'trading'),  
    path('trade/create/', views.create_trading_order, name='create_trading_order'),
    # path('pfx/register', views.PfxRegisterView.as_view(), name = 'pgx_register'), 
    # path('pfx/dashboard', views.Pfxdashbaord.as_view(), name = 'pfx_dashboard'), 
    path('dashboard', views.create_trading_order, name = 'user_dashboard'),

    # UPSTOX
    # path('upstox_auth', views.upstox_auth, name = 'upstox_auth'),  
    path('angelone_auth', views.angelone_authentication, name = 'angelone_auth'),


      
   


      

]