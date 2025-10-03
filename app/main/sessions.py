import Adyen
import json
import uuid
from main.config import get_adyen_api_key, get_adyen_merchant_account

'''
Create Payment Session by calling /sessions endpoint

Request must provide few mandatory attributes (amount, currency, returnUrl, transaction reference)

Your backend should have a payment state where you can fetch information like amount and shopperReference

Parameters
    ----------
    host_url : string
        URL of the host (i.e. http://localhost:8080): required to define returnUrl parameter
'''


def adyen_sessions(host_url):
    # Create and configure the core AdyenClient
    adyen_client = AdyenClient()
    adyen_client.xapikey = get_adyen_api_key()
    adyen_client.platform = "test" # change to live for production
    checkout_service = AdyenCheckoutApi(client=adyen_client)
    
    request = {}

    request['amount'] = {"value": "10000", "currency": "EUR"}  # amount in minor units
    request['reference'] = f"Reference {uuid.uuid4()}"  # provide your unique payment reference
    # set redirect URL required for some payment methods
    request['returnUrl'] = f"{host_url}handleShopperRedirect?shopperOrder=myRef"
    request['countryCode'] = "NL"

    # set lineItems: required for some payment methods (ie Klarna)
    request['lineItems'] = \
        [{"quantity": 1, "amountIncludingTax": 5000, "description": "Sunglasses"}, # amount in minor units
         {"quantity": 1, "amountIncludingTax": 5000, "description": "Headphones"}] # amount in minor units

    request['merchantAccount'] = get_adyen_merchant_account()

    result = checkout_service.payments_api.sessions(request)

    formatted_response = json.dumps((json.loads(result.raw_response)))
    print("/sessions response:\n" + formatted_response)

    return formatted_response
