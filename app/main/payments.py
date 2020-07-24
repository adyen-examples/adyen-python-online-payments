import app.main.config as config
import requests
from random import randint
from flask import json

'''
perform a call to /payments

Taking in the following object from our frontend_request. billingAddress and browserInfo only sent for cards
    {
        paymentMethodData: {
            type: "scheme",
            encryptedCardNumber: "adyenjs_0_1_25$DQ3JeLb...,
            encryptedExpiryMonth: "adyenjs_0_1_25$B1JSCp...,
            encryptedExpiryYear: "adyenjs_0_1_25$h86PBBe...,
            encryptedSecurityCode: "adyenjs_0_1_25$hrwG6...,
            holderName: "Joe Bob"
        },
        billingAddress: {
            street: "Brannan Street",
            city: "San Francisco",
            stateOrProvince: "California",
            postalCode: "94107",
            country: "US",
            houseNumberOrName: 274
        },
        browserInfo: {
            acceptHeader: "*/*",
            colorDepth: 24,
            language: "en-US",
            javaEnabled: false,
            screenHeight: 1440,
            screenWidth: 2560,
            userAgent: "Mozilla/5.0...,
            timeZoneOffset: 480
        }
    };
    
Will use this as the base of our payment request and add the necessary components from our backend. Feel free to modify
these values in the frontend adyen_implementations.js file or to override them here

Returns dictionary representation of JSON response
'''


def adyen_payments(frontend_request):
    url = config.checkout_payments_url

    headers = {"X-Api-Key": config.checkout_apikey, "Content-type": "application/json"}

    payment_methods_request = frontend_request.get_json()
    txvariant = payment_methods_request["paymentMethod"]["type"]

    payment_methods_request["amount"] = {"currency": choose_currency(txvariant),
                                         "value": "1000"}
    payment_methods_request["channel"] = "Web"
    payment_methods_request["merchantAccount"] = config.merchant_account
    payment_methods_request["returnUrl"] = "http://localhost:8080/api/handleShopperRedirect"

    # get reference however you want. For this demo we will hardcode
    # Your reference should be unique. To simulate this, we will append a random int to our reference
    payment_methods_request["reference"] = 'Python Integration Test Reference' + str(randint(0, 10000))
    payment_methods_request["shopperReference"] = 'Python Checkout Shopper'

    payment_methods_request["countryCode"] = 'NL'
    payment_methods_request["shopperLocale"] = "en_US"

    payment_methods_request["storePaymentMethod"] = "true"

    if txvariant == "alipay":
        payment_methods_request["countryCode"] = 'CN'

    elif "klarna" in txvariant:
        payment_methods_request["shopperEmail"] = "myEmail@adyen.com"
        payment_methods_request["lineItems"] = [
            {
                "quantity": "1",
                "amountExcludingTax": "450",
                "taxPercentage": "1111",
                "description": "Sunglasses",
                "id": "Item #1",
                "taxAmount": "50",
                "amountIncludingTax": "500",
                "taxCategory": "High"
            },
            {
                "quantity": "1",
                "amountExcludingTax": "450",
                "taxPercentage": "1111",
                "description": "Headphones",
                "id": "Item #2",
                "taxAmount": "50",
                "amountIncludingTax": "500",
                "taxCategory": "High"
            }]
    elif txvariant == "directEbanking" or txvariant == "giropay":
        payment_methods_request["countryCode"] = "DE"

    elif txvariant == "dotpay":
        payment_methods_request["countryCode"] = "PL"
        payment_methods_request["amount"]["currency"] = "PLN"

    elif txvariant == "scheme":
        payment_methods_request["additionalData"] = {"allow3DS2": "true"}
        payment_methods_request["origin"] = "http://localhost:8080"

    elif txvariant == "ach" or txvariant == "paypal":
        payment_methods_request["countryCode"] = 'US'


    print("/payments request:\n" + str(payment_methods_request))
    r = requests.post(url=url, headers=headers, json=payment_methods_request)
    text_response = r.text
    print("/payments response:\n" + text_response)

    return format_response(r.json())


# Custom payment error class
class PaymentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def choose_currency(payment_method):
    if payment_method == "alipay":
        return "CNY"
    elif payment_method == "dotpay":
        return "PLN"
    elif payment_method == "boletobancario":
        return "BRL"
    elif payment_method == "ach" or payment_method == "paypal":
        return "USD"
    else:
        return "EUR"


# Format response being passed back to frontend. Only leave resultCode and action
def format_response(response):
    if "resultCode" in response:
        new_response = {"resultCode": response["resultCode"]}
        if "action" in response:
            new_response["action"] = response["action"]
        return json.dumps(new_response)
    else:
        raise PaymentError(response)
