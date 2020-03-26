import app.main.config as config
import requests

'''
Retrieve available payment methods by calling /paymentMethods

Request only needs to include merchantAccount, but you can include more information to get a more refined response

Should have a payment state on your server from which you can fetch information like amount and shopperReference
'''


def adyen_payment_methods():
    url = config.checkout_payment_methods_url

    headers = {"X-Api-Key": config.checkout_apikey, "Content-type": "application/json"}

    payment_methods_request = {}
    payment_methods_request["channel"] = "web"
    payment_methods_request["merchantAccount"] = config.merchant_account

    payment_methods_request["reference"] = 'Fusion paymentMethods call'

    print("/paymentMethods request:\n" + str(payment_methods_request))
    r = requests.post(url=url, headers=headers, json=payment_methods_request)
    response = r.text
    print("/paymentMethods response:\n" + response)
    return response
