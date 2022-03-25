# [Adyen Checkout](https://docs.adyen.com/checkout) integration demo

## Run this integration in seconds using [Gitpod](https://gitpod.io/)

* Open your [Adyen Test Account](https://ca-test.adyen.com/ca/ca/overview/default.shtml) and create a set of [API keys](https://docs.adyen.com/user-management/how-to-get-the-api-key).
* Go to [gitpod account variables](https://gitpod.io/variables).
* Set the `ADYEN_API_KEY`, `ADYEN_CLIENT_KEY`, `ADYEN_HMAC_KEY` and `ADYEN_MERCHANT_ACCOUNT variables`.
* Click the button below!

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/adyen-examples/adyen-python-online-payments)

_NOTE: To allow the Adyen Drop-In and Components to load, you have to add gitpod.io as allowed origin for your chosen set of [API Credentials](https://ca-test.adyen.com/ca/ca/config/api_credentials_new.shtml)_

## Details

This repository includes examples of PCI-compliant UI integrations for online payments with Adyen. Within this demo app, we've created a simplified version of an e-commerce website, complete with commented code to highlight key features and concepts of Adyen's API. Check out the underlying code to see how you can integrate Adyen to give your shoppers the option to pay with their preferred payment methods, all in a seamless checkout experience.

![Card Checkout Demo](app/static/img/cardcheckout.gif)

## Supported Integrations

**Python with Flask** demos of the following client-side integrations are available in this repository:

- [Drop-in](https://docs.adyen.com/checkout/drop-in-web)
- [Component](https://docs.adyen.com/checkout/components-web)
  - ACH
  - Alipay
  - Boleto
  - Card
  - Dotpay
  - Giropay
  - iDEAL
  - Klarna
  - PayPal
  - SEPA Direct Debit
  - Sofort

Please make sure to [add the above payment methods to your Adyen account](https://docs.adyen.com/payment-methods#add-payment-methods-to-your-account) before testing!

## Requirements

- Python 3.5 or greater
- Python libraries:
  - flask
  - uuid
  - Adyen v6.0.0 or higher

## Installation

1. Clone this repo

```
git clone https://github.com/adyen-examples/adyen-python-online-payments.git
```

2. Run `source ./setup.sh` to:
   - Create and activate a virtual environment
   - Download the necessary python dependencies

3. Create a `.env` file with all required configuration

   - PORT (default 8080)
   - [API key](https://docs.adyen.com/user-management/how-to-get-the-api-key)
   - [Client Key](https://docs.adyen.com/user-management/client-side-authentication)
   - [Merchant Account](https://docs.adyen.com/account/account-structure)
   - [HMAC Key](https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures)

Remember to include `http://localhost:8080` in the list of Allowed Origins

```
    PORT=8080
    ADYEN_API_KEY="your_API_key_here"
    ADYEN_MERCHANT_ACCOUNT="your_merchant_account_here"
    ADYEN_CLIENT_KEY="your_client_key_here"
    ADYEN_HMAC_KEY="your_hmac_key_here"
```

## Usage
1. Run `./start.sh` to:
   - Initialize the required environment variables. This step is necessary every time you re-activate your venv
   - Start Python app

2. Visit [http://localhost:8080](http://localhost:8080) and select an integration type!

## Contributing

We commit all our new features directly into our GitHub repository. Feel free to request or suggest new features or code changes yourself as well!!

Find out more in our [Contributing](https://github.com/adyen-examples/.github/blob/main/CONTRIBUTING.md) guidelines.

## License

MIT license. For more information, see the **LICENSE** file in the root directory
