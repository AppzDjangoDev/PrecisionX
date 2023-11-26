from __future__ import print_function
import time
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
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin


# # Create your views here.
# class PfxLoginView(View):
#     def get(self, request):
#         template = "profitflow/registration/Login_v1/index.html"
#         context={}
#         context['form']= UserLoginForm()
#         print("context", context)
#         logged_user = request.user

#         if logged_user.is_authenticated:
#             print(logged_user)
#             print("dashboard__form")
#             return redirect('user_dashboard')  
#         else:
#             print(logged_user)
#             print("login__form")
#             return render(request, template, context)
        
#     def logoutUser(request):
#         print("logout_processing")
#         logout(request)
#         return redirect('login')

#     def post(self, request):
#         context={}
#         form = UserLoginForm(request.POST)
#         context['form']= form
#         template ="profitflow/registration/Login_v1/index.html"
#         if request.method == "POST":
#             if form.is_valid():
#                 login_username = request.POST["username"]
#                 login_password = request.POST["password"]
#                 print(login_username)
#                 print(login_password)
#                 user = auth.authenticate(username=login_username, password=login_password)
#                 if user :
#                 # if user is not None and  user.is_superuser==False and user.is_active==True:
#                     auth.login(request, user)
#                     print("login success")
#                     messages.success(request, "Login Successful !")
#                     # return render(request, "user/dashboard.html")
#                     return redirect('user_dashboard')  
#                 else:
#                     print("user not Exists")
#                     # messages.info(request, "user not Exists")
#                     messages.error(request, 'Username or Password incorrect !')
#                     return render(request, template, context)
#             else:
#                 print("user not created")
#                 return render(request, template, context)

# # def homePage(request):
# #     return render(request,'profitflow/index.html')



# class PfxRegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = "landing/register.html"
#     success_url = reverse_lazy('user_dashboard')

#     def form_valid(self, form):
#         response = super().form_valid(form)

#         # Authenticate and log in the user
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password1']
#         messages.success(self.request, 'Registration completed successfully')
#         user = authenticate(username=username, password=password)
#         messages.success(self.request, 'redirected to Dashboard')
#         login(self.request, user)
#         return response
    

# class Pfxdashbaord(View):
#     def get(self, request):
#         template = "profitflow/dashboard/index.html"
#         context={}
#         context['form']= UserLoginForm()
#         print("context", context)
#         logged_user = request.user
#         data=self.getprofiledata(request)

#         if logged_user.is_authenticated:
#             print(logged_user)
#             print("dashboard__form")
#             return redirect('user_dashboard')  
#         else:
#             print(logged_user)
#             print("login__form")
#             return render(request, template, context)
        
#     def UpstoxAuth(self, reuest):
#         import requests
#         # Define variables for the request
#         api_method = 'GET'  # Replace with the desired HTTP method (e.g., GET, POST, PUT, DELETE)
#         api_endpoint = '[API_ENDPOINT]'  # Replace with the specific API endpoint
#         access_token = '[YOUR_ACCESS_TOKEN]'  # Replace with your actual access token
#         content_type_header = {}  # Add content-type header if needed (e.g., 'Content-Type': 'application/json')
#         request_payload = {}  # Add request payload as a dictionary if needed

#         # Define the base URL
#         base_url = 'https://api-v2.upstox.com/'

#         # Construct the full URL
#         url = f'{base_url}{api_endpoint}'

#         # Define headers
#         headers = {
#             'accept': 'application/json',
#             'Api-Version': '2.0',
#             'Authorization': f'Bearer {access_token}'
#         }

#         # Add content-type header if provided
#         headers.update(content_type_header)

#         # Make the HTTP request
#         if api_method == 'GET':
#             response = requests.get(url, headers=headers)
#         elif api_method == 'POST':
#             response = requests.post(url, headers=headers, json=request_payload)
#         elif api_method == 'PUT':
#             response = requests.put(url, headers=headers, json=request_payload)
#         elif api_method == 'DELETE':
#             response = requests.delete(url, headers=headers)
#         else:
#             raise ValueError(f'Unsupported HTTP method: {api_method}')

#         # Check the response
#         if response.status_code == 200:
#             # Successful response
#             response_data = response.json()
#             print(response_data)
#         else:
#             # Handle error response
#             print(f'Request failed with status code {response.status_code}: {response.text}')

        


#     def getprofiledata(self,request):
#         user=request.user
#         print("user__test",user)
#         data ="test"
#         import requests

#         # Define the API endpoint and headers
#         url = 'https://api-v2.upstox.com/user/profile'
#         headers = {
#             'accept': 'application/json',
#             'Api-Version': '2.0',
#             'Authorization': 'Bearer access_token'  # Replace 'access_token' with the actual access token
#         }

#         # Make a GET request
#         response = requests.get(url, headers=headers)

#         # Check if the request was successful (HTTP status code 200)
#         if response.status_code == 200:
#             # Parse and work with the response data
#             profile_data = response.json()
#             print(profile_data)
#         else:
#             print(f"Request failed with status code {response.status_code}: {response.text}")

#         return data

        
#     def logoutUser(request):
#         print("logout_processing")
#         logout(request)
#         return redirect('login')