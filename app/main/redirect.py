import app.main.config as config
import requests
from json import loads

'''
For redirect payment methods, handle redirect back to website

For redirect methods, pull payload from form data
For 3DS payments, pull MD and PaRes from form data

Return response as dictionary to make success/failure redirect in init.py easier
'''


def handle_shopper_redirect(values):
    url = config.checkout_detail_url

    headers = {"X-Api-Key": config.checkout_apikey, "Content-type": "application/json"}

    print("/payments/details request:\n" + str(values))
    r = requests.post(url=url, headers=headers, json=values)
    print("/payments/details response:\n" + r.text)
    return loads(r.text)

