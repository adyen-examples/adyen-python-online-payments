import app.main.config as config
import requests

'''
perform a call to /payments/details

Passing in the component state.data object as frontend_request, This looks like the following:
    {
        details: {
            "threeds2.fingerprint/challengeResult" : "eyJ0aHJlZURTQ29tcEluZCI6IlkifQ==""
        }
        paymentData : "Ab02b4c0!BQABAgB/3ckQEAf5YOdAT83NDjdf+AR4hmjf1fohm2Q8gSe95qb6hE3+GnxfBaK..."
    }
'''


def get_payment_details(frontend_request):
    url = config.checkout_detail_url

    headers = {"X-Api-Key": config.checkout_apikey, "Content-type": "application/json"}

    details = frontend_request.get_json()

    print("/payments/details request:\n" + str(details))
    r = requests.post(url=url, headers=headers, json=details)
    response = r.text
    print("payments/details response:\n" + response)
    return response
