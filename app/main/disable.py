import Adyen
import json
import uuid
from main.config import get_adyen_api_key, get_adyen_merchant_account

'''
Disable payment method by calling the /disable endpoint

Request must provide the mandatory attribute recurringDetail reference to remove  making a payment


Parameters
    ----------
    host_url : string
        URL of the host (i.e. http://localhost:8080): required to define returnUrl parameter
'''
def adyen_disableStoredPayment(data):
    
    adyen = Adyen.Adyen()
    adyen.payment.client.xapikey = get_adyen_api_key()
    adyen.payment.client.platform = "test" # change to live for production
    adyen.payment.client.merchant_account = get_adyen_merchant_account()

    request = {}

    request['recurringDetailReference'] = data
    request['shopperReference'] = f"Reference da356326-7f57-4341-b81c-a8546e8916f4"
    
    
    print("/disable request:\n" + json.dumps(request))

    print("**********************************************************************************")

    result = adyen.recurring.disable(request)

    formatted_response = json.dumps((json.loads(result.raw_response)))
    print("/disable response:\n" + formatted_response)

    print("**********************************************************************************")

    return formatted_response
