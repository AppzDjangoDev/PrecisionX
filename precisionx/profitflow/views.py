from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import http.client
import mimetypes
import http.client
import json
from django.http import JsonResponse
from precisionx import settings
from django.shortcuts import render, redirect
from .forms import TradingOrderForm
from .models import TradingOrder

class Trading_menu(View):
    template_name = 'profitflow/trading.html'

    def get(self, request, *args, **kwargs):
        # Handle GET request logic here
        context = {'message': 'Hello, this is a class-based view!'}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Handle POST request logic here
        return HttpResponse('This is a POST request response.')

    def put(self, request, *args, **kwargs):
        # Handle PUT request logic here
        return HttpResponse('This is a PUT request response.')

def create_trading_order(request):
    if request.method == 'POST':
        form = TradingOrderForm(request.POST)
        if form.is_valid():
            trading_order = form.save(commit=False)
            trading_order.entry_time = get_entry_time()
            trading_order.entry_price = get_entry_price()
            trading_order.save()
            return redirect('success_page')
    else:
        initial_buy_target = get_real_time_option_price()  # Replace with actual implementation
        form = TradingOrderForm(initial={'buy_target': initial_buy_target})
    return render(request, 'accounts/dashboard.html', {'form': form})


def get_entry_time(current_datetime):
    # Implement logic to get entry time from Upstox API or use the current time
    # Replace this with your actual implementation
    return current_datetime

def get_entry_price():
    # Implement logic to get entry price from Upstox API
    # Replace this with your actual implementation
    return 154

def get_real_time_option_price():
    return 0


def upstox_auth(request):
    # Upstox API parameters
    base_url = "https://api-v2.upstox.com"
    client_id = settings.UPSTOX_CLIENT_ID  # Make sure UPSTOX_CLIENT_ID is defined in your settings.py
    print("client_id", client_id)
    redirect_uri = "http://127.0.0.1:8000/trade/create/"
    print("redirect_uri", redirect_uri)
    api_version = "2.0"

    # Redirect URL
    redirect_url = f"{base_url}/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&Api-Version={api_version}"
    print("redirect_urlredirect_urlredirect_url", redirect_url)

    return redirect(redirect_url)




def angelone_authentication(request):
    try:
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
        payload = {
            "clientcode": "CLIENT_ID",
            "password": "CLIENT_PIN",
            "totp": "TOTP_CODE"
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP ,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }
        
        payload_json = json.dumps(payload)
        headers_json = json.dumps(headers)

        conn.request(
            "POST", 
            "/rest/auth/angelbroking/user/v1/loginByPassword",
            payload_json,
            json.loads(headers_json)
        )

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))


        # Check if the response is already a dictionary
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            # If not, create a dictionary with the raw data
            json_data = {'raw_data': data}

        return JsonResponse(json_data, safe=False)  # Set safe=False to allow non-dict objects
    except Exception as e:
        # Handle exceptions
        error_message = str(e)
        response_data = {'error': error_message}
        return JsonResponse(response_data, status=500)

def place_order(request):
    try:
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        payload = {
            "exchange": "NSE",
            "tradingsymbol": "INFY-EQ",
            "quantity": 5,
            "disclosedquantity": 3,
            "transactiontype": "BUY",
            "ordertype": "MARKET",
            "variety": "STOPLOSS",
            "producttype": "INTRADAY"
        }
        headers = {
            'Authorization': 'Bearer AUTHORIZATION_TOKEN',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }

        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def modify_order(request):
    try:
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
        payload = {
            "variety": "NORMAL",
            "orderid": "201020000000080",
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": "194.00",
            "quantity": "1"
        }

        headers = {
            'Authorization': 'Bearer AUTHORIZATION_TOKEN',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }

        conn.request("POST", "/rest/secure/angelbroking/order/v1/modifyOrder", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def get_ltp_data(request):
    try:
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
        payload = {
            "exchange": "NSE",
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": "3045"
        }
        headers = {
            'Authorization': 'Bearer AUTHORIZATION_TOKEN',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }

        conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
