import configparser

'''
Read in variables from config.ini file. Store them as global variables

Make sure to fill out your config.ini file!!!
'''

merchant_account = ""
checkout_apikey = ""
client_key = ""
supported_integrations = ['dropin', 'card', 'ideal', 'klarna', 'directEbanking', 'alipay', 'boletobancario',
                          'sepadirectdebit', 'dotpay', 'giropay', 'ach', 'paypal', 'applepay', 'directdebit_GB']


def read_config():
    global merchant_account, checkout_apikey, client_key

    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    merchant_account = config['DEFAULT']['merchant_account']
    checkout_apikey = config['DEFAULT']['apikey']
    client_key = config['DEFAULT']['client_key']

    # Check to make sure variables are set
    if not merchant_account or not checkout_apikey or not client_key:
        raise Exception("Please fill out information in config.ini file")
