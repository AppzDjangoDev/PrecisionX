from datetime import datetime, timedelta
import os
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
import pyotp
import requests  # Don't forget to import the requests module
from django.middleware.csrf import get_token


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
            get_market_data = fetch_market_data(request)
            print("oooooooooooo", get_market_data)
            # Print form data
            post_data = dict(form.cleaned_data.items())
            # Accessing values using keys
            stock_name = post_data.get('stock_name', '')
            option_type = post_data.get('option_type', '')
            strike_type = post_data.get('strike_type', '')
            buy_target = str(post_data.get('buy_target', ''))  # Convert to string
            stop_loss = post_data.get('stop_loss', '')
            trailing_stop_loss_interval = post_data.get('trailing_stop_loss_interval', '')
            trailing_stop_loss = post_data.get('trailing_stop_loss', '')

            # Print or use the values as needed
        
            print(f"Stock Name: {stock_name}")
            print(f"Option Type: {option_type}")
            print(f"Strike Type: {strike_type}")
            print(f"Buy Target: {buy_target}")
            print(f"Stop Loss: {stop_loss}")
            print(f"Trailing Stop Loss Interval: {trailing_stop_loss_interval}")
            print(f"Trailing Stop Loss: {trailing_stop_loss}")
            # Extract JSON content from JsonResponse
            json_data = json.loads(get_market_data.content)
            # Extract ltp from the data
            ltp = json_data.get('data', {}).get('fetched', [{}])[0].get('ltp')
            print("ppppppppppppppppppppppppppppp", ltp)
            # get_order_name_here 
            option_name = generate_option_order_name(stock_name,ltp)
            print("7777777777777777777777777777777", option_name)
            option_name = option_name+option_type
            options_data = fetch_market_data(request, option_name)
            print("options_data", options_data)



















            trading_order = form.save(commit=False)
            trading_order.entry_time = get_entry_time()
            trading_order.entry_price = get_entry_price()
            trading_order.save()
            return redirect('success_page')
        
    else:
        initial_buy_target = 0
        form = TradingOrderForm(initial={'buy_target': initial_buy_target})
    return render(request, 'accounts/dashboard.html', {'form': form})


def get_entry_time():
    current_datetime = datetime.now()
    return current_datetime

def get_entry_price():
    # Implement logic to get entry price from  API
    # Replace this with your actual implementation
    return 154


def find_nearest_strike_price(current_ltp):
    # Find the closest value divisible by 50
    strike_price = round(current_ltp / 50) * 50
    return strike_price

def generate_option_order_name(indices_name, current_ltp):
    # Get the nearest strike price divisible by 50
    strike_price = find_nearest_strike_price(current_ltp)

    # Get the current date and time
    current_datetime = datetime.now()

    # # Check if today is Thursday
    # is_thursday = current_datetime.weekday() == 3  # Monday is 0 and Sunday is 6

    # Calculate the next Thursday's date
    days_until_thursday = (3 - current_datetime.weekday() + 7) % 7
    next_thursday = current_datetime + timedelta(days=days_until_thursday)

    # Format the expiry date in the required format (e.g., 07DEC20)
    expiry_date = next_thursday.strftime("%d%b%y").upper()

    # Include is_thursday in the option trading name if needed
    option_trading_name = f"{indices_name}{expiry_date}{strike_price}"

    return option_trading_name, strike_price


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

        jwt_token = request.session.get('jwt_token', None)
        headers = {
            'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
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
    
def search_symbol_in_json(symbol):
    print("symbol", symbol, "symbol__typoe", type(symbol))
    # Example usage
    # Get the path to the JSON file in the same directory as views.py
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, 'market_data.json')
    # Read data from the JSON file
    with open(json_file_path, 'r') as file:
        market_data = json.load(file)

    for entry in market_data:
        if entry.get("symbol") == symbol:
            print("gooooooooooooooooooooooooooooooooooooooooooooooooo")
            return entry
    # Return None if symbol is not found
    return None

def search_symbols_in_json(symbols):
    # Example usage
    # Get the path to the JSON file in the same directory as views.py
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, 'market_data.json')
    # Read data from the JSON file
    with open(json_file_path, 'r') as file:
        market_data = json.load(file)

    result = []
    
    for symbol in symbols:
        for entry in market_data:
            if entry.get("symbol") == symbol:
                result.append(entry)
                print("Symbol", symbol, "found!")
                break  # Exit the inner loop once the symbol is found

    # Return the list of matching entries, or an empty list if no matches are found
    return result

from django.http import JsonResponse
# widget data
def get_strike_widget_data(request):
    option_types=["CE","PE"]
    stock_name="NIFTY"
    current_nifty_data = get_nifty_ltp_data(request)
    # Accessing the JsonResponse content
    json_data = current_nifty_data.content
    # Convert the JSON string to a Python dictionary using json.loads
    data_dict = json.loads(json_data)
    # Accessing specific values
    ltp = data_dict.get('data', {}).get('ltp')
    print("LTP:", ltp)
    # get_order_name_here 
    option_name_list = []
    option_name, strike_price = generate_option_order_name(stock_name,ltp)
    for option_type in option_types:
        updated_option_name = option_name+option_type
        option_name_list.append(updated_option_name)

    options_data = fetch_market_data(request,option_name_list, strike_price)
    print("options_dataoptions_data", options_data)
    # Include strike_price in the options_data
    fetched_data = options_data.get('data', {}).get('fetched', [])
    for option in fetched_data:
        option['strike_price'] = strike_price

    print("__________________________________________________")
    print("options_data:", options_data, "type:", options_data)
    return options_data


def get_nifty_ltp_data(request, exchange="NSE", tradingsymbol="NIFTY", symboltoken="99926000"):
    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    payload = {
        "exchange": exchange,
        "tradingsymbol": tradingsymbol,
        "symboltoken": symboltoken
    }
    jwt_token = request.session.get('jwt_token', None)
    headers = {
        'X-PrivateKey': settings.ANGELONE_APIKEY,
        'Accept': 'application/json',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': settings.LOCAL_IP,
        'X-ClientPublicIP': settings.PUBLIC_IP,
        'X-MACAddress': settings.MAC_ADDRESS,
        'X-UserType': 'USER',
        'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
        'Content-Type': 'application/json'
    }
    # Convert payload to JSON string
    payload_str = json.dumps(payload)
    conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", payload_str, headers)
    # Get the response
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    try:
        # Try to parse the response as JSON
        json_data = json.loads(data)
    except json.JSONDecodeError:
        # If not a JSON response, create a dictionary with the raw data
        json_data = {'raw_data': data}
    return JsonResponse(json_data,  safe=False)  # Set safe=False to allow non-dict objects



def fetch_market_data(request, option_name_list=None,strike_price=None):
    # try:
    # Define the connection details
    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
    if option_name_list:
        option_data = search_symbols_in_json(option_name_list)
        token_dict = {"NFO":[]}
        token_list = []
        for data  in option_data:
            token_list.append(data['token'])
            
        token_dict['NFO']=token_list
        payload = {
            "mode": "LTP",
            "exchangeTokens": token_dict
        }
    else:
        # nedd to add current strike and put and call ltp with it 
        # GET CURRENT STRIKE TOKEN
        payload = {
            "mode": "FULL",
            "exchangeTokens": {
                "NSE": ["99926000"], "NFO": ["43173", "43175"]
            }
        }

    jwt_token = request.session.get('jwt_token', None)
    # Define the headers for the request
    headers = {
        'X-PrivateKey': settings.ANGELONE_APIKEY,
        'Accept': 'application/json',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': settings.LOCAL_IP,
        'X-ClientPublicIP': settings.PUBLIC_IP,
        'X-MACAddress': settings.MAC_ADDRESS,
        'X-UserType': 'USER',
        'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
        'Content-Type': 'application/json'
    }

    # Convert payload and headers to JSON strings
    payload_json = json.dumps(payload)

    # Make the POST request
    conn.request("POST", "/rest/secure/angelbroking/market/v1/quote/", payload_json, headers)

    # Get the response
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    print("xxxxxxxxxxx", data, "xxxxxxxxxxxxxxtype", type(data))

    try:
        # Try to parse the response as JSON
        json_data = json.loads(data)
        json_data["strike_price"] = strike_price
        print("json_datajson_data", json_data, type(json_data))
    except json.JSONDecodeError:
        # If not a JSON response, create a dictionary with the raw data
        json_data = {'raw_data': data}

    return JsonResponse(json_data, safe=False)  # Set safe=False to allow non-dict objects
# ********************************************************************************************


from django.http import JsonResponse

def check_session_values(request):
    try:
        # Define the keys you want to check in the session
        required_keys = ['jwt_token', 'refresh_token', 'feed_token']
        # Check if all required keys are present in the session
        if all(key in request.session for key in required_keys):
            # All required keys are present
            response_data = {'status': 200, 'message': 'All session values are present'}
        else:
            # Some or all required keys are missing
            response_data = {'status': 500, 'message': 'Some session values are missing'}
        # Return the response_data
        return response_data
    except Exception as e:
        # Handle exceptions
        error_message = str(e)
        response_data = {'status': 500, 'message': 'Some session values are missing'}

def check_api_status(request):
    try:
        response_data = check_session_values(request)
        if response_data:
            return JsonResponse(response_data)
    except Exception as e:
        # Handle exceptions
        error_message = str(e)
        response_data = {'error': error_message}
        return JsonResponse(response_data, status=500)


def get_tokens_from_session(request):
    jwt_token = request.session.get('jwt_token', None)
    refresh_token = request.session.get('refresh_token', None)
    feed_token = request.session.get('feed_token', None)
    return jwt_token, refresh_token, feed_token


def set_tokens_in_session(request, jwt_token, refresh_token, feed_token):
    request.session['jwt_token'] = jwt_token
    request.session['refresh_token'] = refresh_token
    request.session['feed_token'] = feed_token

def clear_session_values(request):
    try:
        # Remove specific keys from the session
        request.session.pop('jwt_token', None)
        request.session.pop('refresh_token', None)
        request.session.pop('feed_token', None)
        return JsonResponse({'status': 'success', 'message': 'Session values cleared successfully'})

    except Exception as e:
        # Handle exceptions
        error_message = str(e)
        response_data = {'error': error_message}
        return JsonResponse(response_data, status=500)

def angelone_authentication(request):
    # try:
    # Ensure that the request method is POST
    if request.method == 'POST':
        mpin = request.POST.get('password', '')
        totp = pyotp.TOTP(settings.ANGELONE_TOTP_SECRET).now()

        payload = {
            "clientcode": settings.ANGELONE_CLIENT_ID,
            "password": mpin,
            "totp": totp
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

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
        # Parse the data string into a dictionary
        data_dict = json.loads(data.decode("utf-8"))

        # Check if 'data' key exists in the dictionary
        if 'data' in data_dict and isinstance(data_dict['data'], dict):
            jwt_token = data_dict['data'].get('jwtToken', '')
            refresh_token = data_dict['data'].get('refreshToken', '')
            feed_token = data_dict['data'].get('feedToken', '')
        # Set tokens in session
        set_tokens_in_session(request, jwt_token, refresh_token, feed_token)
        # Check if the response is already a dictionary
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            # If not, create a dictionary with the raw data
            json_data = {'raw_data': data}

        return JsonResponse(json_data, safe=False)  # Set safe=False to allow non-dict objects
    else:
        # Return a 405 Method Not Allowed response for non-POST requests
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def angelone_logout(request):
    try:
        # Get the CSRF token
        csrf_token = get_token(request)

        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        payload = {
            "clientcode": settings.ANGELONE_CLIENT_ID,
        }

        jwt_token = request.session.get('jwt_token', None)
        headers = {
            'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY,
            'X-CSRFToken': csrf_token  # Include the CSRF token in the headers
        }

        payload_json = json.dumps(payload)

        conn.request("POST", "/rest/secure/angelbroking/user/v1/logout", payload_json, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
        clear_session_values(request)
        return JsonResponse({'message': 'Logout successful'})

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)}, status=500)

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

        jwt_token = request.session.get('jwt_token', None)
        headers = {
            'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
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

        jwt_token = request.session.get('jwt_token', None)
        headers = {
            'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
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

def get_user_profile(request):
    try:
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
        payload = ''
        

        jwt_token = request.session.get('jwt_token', None)
        headers = {
            'Authorization': f'Bearer {jwt_token}' if jwt_token else None,
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': settings.LOCAL_IP,
            'X-ClientPublicIP': settings.PUBLIC_IP,
            'X-MACAddress': settings.MAC_ADDRESS,
            'X-PrivateKey': settings.ANGELONE_APIKEY
        }
        
        conn.request("GET", "/rest/secure/angelbroking/user/v1/getProfile", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    except Exception as e:
        print(f"An error occurred: {e}")
