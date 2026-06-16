import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ADYEN_WEB_VERSION = "6.6.0"
ADYEN_CHECKOUT_APPLICATION_NAME = (
    f"adyen-python-online-payments checkout-example adyen-web/{ADYEN_WEB_VERSION}"
)


def get_port():
    return os.environ.get("PORT", 8080)


def get_adyen_merchant_account():
    adyen_merchant_account = os.environ.get("ADYEN_MERCHANT_ACCOUNT")

    if not adyen_merchant_account:
        raise Exception("Missing ADYEN_MERCHANT_ACCOUNT in .env")

    return adyen_merchant_account


def get_adyen_api_key():
    adyen_api_key = os.environ.get("ADYEN_API_KEY")

    if not adyen_api_key:
        raise Exception("Missing ADYEN_API_KEY in .env")

    return adyen_api_key


def get_adyen_client_key():
    adyen_client_key = os.environ.get("ADYEN_CLIENT_KEY")

    if not adyen_client_key:
        raise Exception("Missing ADYEN_CLIENT_KEY in .env")

    return adyen_client_key


def get_adyen_hmac_key():
    adyen_hmac_key = os.environ.get("ADYEN_HMAC_KEY")

    if not adyen_hmac_key:
        raise Exception("Missing ADYEN_HMAC_KEY in .env")

    return adyen_hmac_key


def configure_adyen_client(adyen_client):
    adyen_client.xapikey = get_adyen_api_key()
    adyen_client.platform = "test"

    user_agent_prefix = f"{ADYEN_CHECKOUT_APPLICATION_NAME} "
    if not adyen_client.USER_AGENT_SUFFIX.startswith(user_agent_prefix):
        adyen_client.USER_AGENT_SUFFIX = user_agent_prefix + adyen_client.USER_AGENT_SUFFIX

    return adyen_client


def get_supported_integration():
    return ['dropin', 'card', 'ideal', 'klarna', 'directEbanking', 'alipay', 'boletobancario',
            'sepadirectdebit', 'dotpay', 'giropay', 'ach', 'paypal', 'applepay',
            'klarna_paynow', 'klarna', 'klarna_account']


    # Check to make sure variables are set
    # if not merchant_account or not checkout_apikey or not client_key or not hmac_key:
    #     raise Exception("Incomplete configuration in .env")
