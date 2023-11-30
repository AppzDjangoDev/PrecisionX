from django.shortcuts import redirect, render
from accounts.forms import UserLoginForm, UserprofileUpdate
from django.contrib import auth
from django.views import View  
from django.contrib.auth import logout
from django.contrib import messages
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import re



# Create your views here.
class UserloginView(View):
    def get(self, request):
        self.template = "accounts/login.html"
        context={}
        context['form']= UserLoginForm()
        print("context", context)
        logged_user = request.user

        if logged_user.is_authenticated:
            print(logged_user)
            print("dashboard__form")
            return redirect('create_trading_order')  
        else:
            print(logged_user)
            print("login__form")
            return render(request, self.template, context)
        
    def logoutUser(request):
        print("logout_processing")
        logout(request)
        return redirect('login')
    
    def post(self, request):
        self.template = "accounts/login.html"
        form = UserLoginForm(request.POST)
        context = {'form': form}
        print("entry00")

        if form.is_valid():
            print("enter1")
            login_username = request.POST.get("username")
            login_password = request.POST.get("password")
            print("login_username", login_username,"login_password", login_password )
            user = authenticate(username=login_username, password=login_password)
            print("useruser", user)
            if user:
                print("user>>>>>>>>", user)
                auth.login(request, user)
                messages.success(request, "Login Successful!")
                return redirect('create_trading_order')
            else:
                messages.error(request, 'Username or Password incorrect!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")

            messages.error(request, 'Form data is invalid')
        return render(request, self.template, context)
        
def HomePage(request):
    return render(request,'profitflow/home.html')


def LandingPage(request):
    return render(request,'landing/index.html')



class UserRegistrationView(CreateView):
    print("00000000000000000000")
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy('user_dashboard')
    print("entry001")
    def post(self, request , **kwargs):
        success_url = reverse_lazy('user_dashboard')
        template_name = "accounts/register.html"
        print("request.method ", request.POST )
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()  # Save the user
                # You can also log the user in here if needed
                # return redirect(success_url)
            else:
                print("pppp",form.errors)
                # return redirect(success_url)
        else:
            form = CustomUserCreationForm()

        return render(request,template_name, {'form': form})
    
class MemberListView(View):
    def get(self, request , **kwargs):
        template = "accounts/accountsmanage.html"
        breadcrumb = {"1":"Member Management", "2":"Manage member" }
        label = { 'title' : "Manage member" }
        header = { "one": 'First Name',"two" : 'Last Name', "three" : "User Name",}
        Data =  User.objects.all()
        context = {'header':header , 'label':label, "breadcrumb":breadcrumb ,"Data": Data}
        return render(request, template, context)

class SuccessView(View):
    def get(self, request):
        template = "success_page.html"
        context={}
        print("context", context)
        return render(request, template, context)
        
# @login_required(login_url='/login/')
class UserDashBoardView(LoginRequiredMixin,View):
    def get(self, request):
        template = "accounts/dashboard.html"
        context={}
        pass

        print("context", context)
        return render(request, template, context)

class ProfileView(View):
    def __init__(self):
        pass

    def get(self, request):
        user_pk = request.user
        try:
            instance = User.objects.get(pk=user_pk.id)
        except User.DoesNotExist:
            instance = None
        form = UserprofileUpdate(instance=instance)
        template = "accounts/pages-accounts-settings-accounts.html"
        context={}
        context['form'] = form
        print("context", context)
        return render(request, template, context)

    def post(self, request):
        user_id = request.user.id
        instance = get_object_or_404(User, id=user_id)
        context={}
        form = UserprofileUpdate(request.POST or None, request.FILES or None,  instance=instance)
        context['form']= form
        template = "accounts/pages-accounts-settings-accounts.html"
        if form.is_valid():
            form.save()
            print("updated successfully")
            messages.success(request, 'Your accounts details updated successfully!')
            return redirect('user_dashboard')  
        else:
            print("updating failed")
            return render(request, template, context)