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
    # path('angelone_auth', views.angelone_authentication, name = 'angelone_auth'),
    # path('check-api-status/', views.check_api_status, name='check_api_status'),
    # path('logout/', views.angelone_logout, name='logout'),
    # path('get_market_data/', views.get_nifty_ltp_data, name='get_market_data'),
    # path('get_strike_widget_data/', views.get_strike_widget_data, name='get_strike_widget_data'),

    


      
   


      

]