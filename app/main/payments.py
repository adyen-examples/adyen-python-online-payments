import app.main.config as config
import requests
from random import randint
from flask import json

'''
perform a call to /payments

Passing in the following object as frontend_request
    {
        amount: getAmount(),
        browserInfo: {
            shopperReference: getShopperReference(),
            colorDepth: screen.colorDepth,
            screenHeight: screen.height,
            screenWidth: screen.width,
            timeZoneOffset: dt.getTimezoneOffset()
        }
    };
    
Will use this as the base of our payment request and add the necessary components from our backend

Returns dictionary representation of JSON response
'''


def initiate_payment(frontend_request):
    url = config.checkout_payments_url

    headers = {"X-Api-Key": config.checkout_apikey, "Content-type": "application/json"}

    payment_methods_request = frontend_request.get_json()
    payment_methods_request["channel"] = "Web"
    payment_methods_request["merchantAccount"] = config.merchant_account
    payment_methods_request["returnUrl"] = "http://localhost:5000/handleShopperRedirect"

    # get reference however you want. For this demo we will hardcode
    # Your reference should be unique. To simulate this, we will append a random int to our reference
    payment_methods_request["reference"] = 'Fusion Reference' + str(randint(0, 10000))

    if payment_methods_request["paymentMethod"]["type"] != "ideal":
        ip_address = frontend_request.environ.get('HTTP_X_REAL_IP', frontend_request.remote_addr)

        # resolve country code/location from ip_address however you want. Will hardcode for this example to 'NL'
        payment_methods_request["countryCode"] = 'NL'

        # TODO: Adding browserInfo component, utilize when released
        payment_methods_request["browserInfo"]["userAgent"] = frontend_request.headers.get('User-Agent')
        payment_methods_request["browserInfo"]["acceptHeader"] = frontend_request.headers.get('Accept')
        payment_methods_request["browserInfo"]['language'] = frontend_request.headers.get('Accept-language')

        payment_methods_request["additionalData"] = {"allow3DS2": True}

        payment_methods_request["origin"] = "http://localhost:5000"

    # Klarna local payment method requires us to specify line items with tax information, they're hardcoded
    # for this specific example here. For more information, see https://docs.adyen.com/payment-methods/klarna
    if payment_methods_request["paymentMethod"]["type"] == "klarna":
        payment_methods_request["lineItems"] = [
            {
                "quantity": "1",
                "amountExcludingTax": "413",
                "taxPercentage": "2100",
                "description": "Sunglasses",
                "id": "Item #1",
                "taxAmount": "87",
                "amountIncludingTax": "500",
                "taxCategory": "High"
            },
            {
                "quantity": "1",
                "amountExcludingTax": "413",
                "taxPercentage": "2100",
                "description": "Headphones",
                "id": "Item #2",
                "taxAmount": "87",
                "amountIncludingTax": "500",
                "taxCategory": "High"
            }]

    print("/payments request:\n" + str(payment_methods_request))
    r = requests.post(url=url, headers=headers, json=payment_methods_request)
    text_response = r.text
    print("/payments response:\n" + text_response)

    return format_response(r.json())


# Format response being passed back to frontend. Only leave resultCode and action
def format_response(response):
    new_response = {"resultCode": response["resultCode"]}
    if "action" in response:
        new_response["action"] = response["action"]
    return json.dumps(new_response)

