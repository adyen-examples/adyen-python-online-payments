import app.main.config as config
import Adyen
import json

'''
Create Payment Session by calling /sessions

Request must provide few mandatory attributes (merchantAccount, amount, returnUrl, transaction reference)

Your backend should have a payment state where you can fetch information like amount and shopperReference
'''


def adyen_sessions():
    adyen = Adyen.Adyen()
    adyen.client.platform = 'test'
    adyen.client.xapikey = config.checkout_apikey
    adyen.client.app_name = 'myapp'

    request = {}

    request['amount'] = {"value": "1000", "currency": "EUR"}
    request['reference'] = "YOUR_PAYMENT_REFERENCE"
    request['merchantAccount'] = config.merchant_account
    request['returnUrl'] = "https://your-company.com/checkout?shopperOrder=12xy.."
    request['countryCode'] = "NL"

    result = adyen.checkout.sessions(request)

    formatted_response = json.dumps((json.loads(result.raw_response)))
    print("/sessions response:\n" + formatted_response)

    return formatted_response
