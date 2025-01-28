# Sample app with Adyen Adyen Web 5.68.x.

This folder contains the previous version of the sample application that uses **Adyen Web 5.68.x**.

Check the root folder of the repository to use the latest Adyen Web 6.x

## Details

This repository showcases a PCI-compliant integration of the [Sessions Flow](https://docs.adyen.com/online-payments/build-your-integration/additional-use-cases/), the default integration that we recommend for merchants. Explore this simplified e-commerce demo to discover the code, libraries and configuration you need to enable various payment options in your checkout experience.  

![Card Checkout Demo](app/static/img/cardcheckout.gif)

The Demo leverages Adyen's API Library for Python [GitHub](https://github.com/Adyen/adyen-python-api-library) | [Docs](https://github.com/Adyen/adyen-python-api-library).

## Requirements

- Python 3.5 or greater
- Python libraries:
  - flask
  - uuid
  - Adyen v12.0.0 or higher

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

2. Visit [http://localhost:8080](http://localhost:8080) and select an integration type.

To try out integrations with test card numbers and payment method details, see [Test card numbers](https://docs.adyen.com/development-resources/test-cards/test-card-numbers).

# Webhooks

Webhooks deliver asynchronous notifications about the payment status and other events that are important to receive and process. 
You can find more information about webhooks in [this blog post](https://www.adyen.com/knowledge-hub/consuming-webhooks).

### Webhook setup

In the Customer Area under the `Developers → Webhooks` section, [create](https://docs.adyen.com/development-resources/webhooks/#set-up-webhooks-in-your-customer-area) a new `Standard webhook`.

A good practice is to set up basic authentication, copy the generated HMAC Key and set it as an environment variable. The application will use this to verify the [HMAC signatures](https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures/).

Make sure the webhook is **enabled**, so it can receive notifications.

### Expose an endpoint

This demo provides a simple webhook implementation exposed at `/api/webhooks/notifications` that shows you how to receive, validate and consume the webhook payload.

### Test your webhook

The following webhooks `events` should be enabled:
* **AUTHORISATION**


To make sure that the Adyen platform can reach your application, we have written a [Webhooks Testing Guide](https://github.com/adyen-examples/.github/blob/main/pages/webhooks-testing.md)
that explores several options on how you can easily achieve this (e.g. running on localhost or cloud).

