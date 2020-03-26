import configparser

'''
Read in variables from config.ini file. Store them as global variables

Make sure to fill out your config.ini file!!!
'''

merchant_account = ""
checkout_apikey = ""
origin_key = ""
checkout_payment_methods_url = ""
checkout_payments_url = ""
checkout_detail_url = ""
supported_integrations = ['dropin', 'card', 'ideal', 'klarna', 'directEbanking', 'alipay', 'wechatpayWeb',
                                  'boletobancario', 'sepadirectdebit', 'dotpay', 'giropay', 'ach']


def read_config():
    global merchant_account, checkout_apikey, origin_key, checkout_payments_url, checkout_detail_url, \
        checkout_payment_methods_url

    config = configparser.ConfigParser()
    config.read('config.ini')

    merchant_account = config['DEFAULT']['merchant_account']
    checkout_apikey = config['DEFAULT']['checkout_apikey']
    origin_key = config['DEFAULT']['origin_key']
    checkout_payment_methods_url = config['DEFAULT']['checkout_payment_methods_url']
    checkout_payments_url = config['DEFAULT']['checkout_payments_url']
    checkout_detail_url = config['DEFAULT']['checkout_detail_url']

    # Check to make sure variables are set
    if not merchant_account or not checkout_apikey or not origin_key or not checkout_payment_methods_url or not \
            checkout_payments_url or not checkout_detail_url:
        raise Exception("Please fill out information in config.ini file")
