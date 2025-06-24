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
    adyen = Adyen.Adyen()
    adyen.payment.client.xapikey = get_adyen_api_key()
    adyen.payment.client.platform = "live"
    adyen.client.live_endpoint_prefix = "8949b923f75af6b1-AdyenTechSupportIndia"
    adyen.payment.client.merchant_account = get_adyen_merchant_account()

    request = {}

    request['amount'] = {"value": "10000", "currency": "INR"}  # amount in minor units
    request['reference'] = f"Reference {uuid.uuid4()}"  # provide your unique payment reference
    # set redirect URL required for some payment methods
    request['returnUrl'] = f"{host_url}handleShopperRedirect?shopperOrder=myRef"
    request['countryCode'] = "IN"

    # set lineItems: required for some payment methods (ie Klarna)
    request['lineItems'] = \
        [{"quantity": 1, "amountIncludingTax": 5000, "description": "Sunglasses"}, # amount in minor units
         {"quantity": 1, "amountIncludingTax": 5000, "description": "Headphones"}] # amount in minor units

    request['merchantAccount'] = get_adyen_merchant_account()

    result = adyen.checkout.payments_api.sessions(request)

    formatted_response = json.dumps((json.loads(result.raw_response)))
    print("/sessions response:\n" + formatted_response)

    return formatted_response
