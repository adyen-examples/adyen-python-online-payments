# [Adyen Checkout](https://docs.adyen.com/checkout) integration demo

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
  - Adyen

## Installation

1. Clone this repo
2. Navigate to root level of repo
3. Run `source ./setup.sh` to:
   - Create and activate a virtual environment
   - Download the necessary python dependencies

## Usage

1. Run `./setup.sh` to install dependencies and to activate your `venv` if you haven't done already in above steps
2. Update the config file `config.ini` with your [API key](https://docs.adyen.com/user-management/how-to-get-the-api-key), [Client Key](https://docs.adyen.com/user-management/client-side-authentication) - Remember to add `http://localhost:8080` as an origin for client key, and merchant account name like below:
   ```
   merchant_account = TestMerchantAccount
   checkout_apikey = SampleAPIKey
   client_key = SampleClientKey
   ```
3. Run `./start.sh` to:
   - Initialize the required environment variables. This step is necessary every time you re-activate your (venv)
   - Run flask
4. Visit [http://localhost:8080](http://localhost:8080) and select an integration type!

## Contributing

We commit all our new features directly into our GitHub repository. Feel free to request or suggest new features or code changes yourself as well!!

## License

MIT license. For more information, see the **LICENSE** file in the root directory
