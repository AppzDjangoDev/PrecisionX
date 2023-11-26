from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint




APIKEY="291943be-4127-4882-8a4f-ecaba1af4457"
SECRET="w7epn6vyk3"



# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = APIKEY

# create an instance of the API class
api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = SECRET # str | Key of the instrSument
quantity = 1 # int | Quantity with which the order is to be placed
product = 'product_example' # str | Product with which the order is to be placed
transaction_type = 'transaction_type_example' # str | Indicates whether its a BUY or SELL order
price = 3.4 # float | Price with which the order is to be placed
api_version = 'api_version_example' # str | API Version Header

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)