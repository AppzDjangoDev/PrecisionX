from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import UserRegistrationView


urlpatterns = [
    # landing page
    path('', views.LandingPage, name = 'home'),
    # login 
    path('login', views.UserloginView.as_view(), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('register', views.UserRegisterView.as_view(), name = 'user_registration'),
    path('register', UserRegistrationView.as_view(), name='user_registration'),
    # dashboard 
    path('dashboard', views.UserDashBoardView.as_view(), name = 'user_dashboard'),
    path("profile-view", views.ProfileView.as_view(), name="profile_view"),

    # manage member 
    path("member-manage", views.MemberListView.as_view(), name="member_manage"),

    
    


      
   


      

]