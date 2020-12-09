import app.main.config as config
import Adyen
import json

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
    formatted_response = json.dumps((json.loads(payment_methods_response.raw_response)))
    
    print("/paymentMethods response:\n" + formatted_response)
    return formatted_response
