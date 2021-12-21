import app.main.config as config
import Adyen
import json
import uuid

'''
Create Payment Session by calling /sessions endpoint

Request must provide few mandatory attributes (amount, currency, returnUrl, transaction reference)

Your backend should have a payment state where you can fetch information like amount and shopperReference
'''


def adyen_sessions():
    adyen = Adyen.Adyen()
    adyen.payment.client.xapikey = config.checkout_apikey
    adyen.payment.client.platform = "test" # change to live for production
    adyen.payment.client.merchant_account = config.merchant_account

    request = {}

    request['amount'] = {"value": "1000", "currency": "EUR"}
    request['reference'] = f"Reference {uuid.uuid4()}"  # provide your unique payment reference
    # set redirect URL required for some payment methods
    request['returnUrl'] = f"http://localhost:8080/redirect?shopperOrder=myRef"
    request['countryCode'] = "NL"

    result = adyen.checkout.sessions(request)

    formatted_response = json.dumps((json.loads(result.raw_response)))
    print("/sessions response:\n" + formatted_response)

    return formatted_response
