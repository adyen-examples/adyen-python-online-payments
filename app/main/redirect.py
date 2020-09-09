import app.main.config as config
import Adyen
import json
from .payment_methods import format_for_json

'''
For redirect payment methods, handle redirect back to website

For redirect methods, pull payload from form data
For 3DS payments, pull MD and PaRes from form data

Return response as dictionary to make success/failure redirect in init.py easier
'''


def handle_shopper_redirect(values):
    adyen = Adyen.Adyen()
    adyen.payment.client.platform = "test"
    adyen.client.xapikey = config.checkout_apikey
    
    details_request = values
    
    print("/payments/details request:\n" + str(details_request))
    
    details_response = adyen.checkout.payments_details(details_request)
    formatted_response = format_for_json(details_response)
    
    print("payments/details response:\n" + formatted_response)
    return json.loads(formatted_response)
    

