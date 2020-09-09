import app.main.config as config
import Adyen
from functools import reduce


'''
Retrieve available payment methods by calling /paymentMethods

Request only needs to include merchantAccount, but you can include more information to get a more refined response

Should have a payment state on your server from which you can fetch information like amount and shopperReference
'''


def adyen_payment_methods():
    adyen = Adyen.Adyen()
    adyen.client.platform = 'test'
    adyen.client.xapikey = config.checkout_apikey

    payment_methods_request = {
        'merchantAccount': config.merchant_account,
        'reference': 'Fusion paymentMethods call',
        'shopperReference': 'Python Checkout Shopper',
        'channel': 'Web',
    }
    
    print("/paymentMethods request:\n" + str(payment_methods_request))

    payment_methods_response = adyen.checkout.payment_methods(payment_methods_request)
    formatted_response = format_for_json(payment_methods_response)
    
    print("/paymentMethods response:\n" + formatted_response)
    return formatted_response


# Raw AdyenResult object isn't proper JSON. This function formats the response to proper JSON
def format_for_json(response):
    replace_dict = ("'", "\""), ("True", "true"), ("False", "false")
    return reduce(lambda a, kv: a.replace(*kv), replace_dict, str(response))


