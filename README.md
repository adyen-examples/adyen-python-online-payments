# Adyen Python [Online Payment](https://docs.adyen.com/online-payments) integration demos

[![Python Build](https://github.com/adyen-examples/adyen-python-online-payments/actions/workflows/build.yml/badge.svg)](https://github.com/adyen-examples/adyen-python-online-payments/actions/workflows/build.yml) 
[![E2E (Playwright)](https://github.com/adyen-examples/adyen-python-online-payments/actions/workflows/e2e.yml/badge.svg)](https://github.com/adyen-examples/adyen-python-online-payments/actions/workflows/e2e.yml)

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

## Quick Start with GitHub Codespaces

This repository is configured to work with [GitHub Codespaces](https://github.com/features/codespaces). Click the badge below to launch a Codespace with all dependencies pre-installed.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new/adyen-examples/adyen-python-online-payments?ref=main&devcontainer_path=.devcontainer%2Fdevcontainer.json)

For detailed setup instructions, see the [GitHub Codespaces Instructions](https://github.com/adyen-examples/.github/blob/main/pages/codespaces-instructions.md).

## Local Installation

1. Clone this repo:

```
git clone https://github.com/adyen-examples/adyen-python-online-payments.git
```

2. Run `source ./setup.sh` to:
   - Create and activate a virtual environment
   - Download the necessary python dependencies

3. Set the following environment variables in your terminal:

  - PORT (default 8080)
  - [API key](https://docs.adyen.com/user-management/how-to-get-the-api-key)
  - [Client Key](https://docs.adyen.com/user-management/client-side-authentication)
  - [Merchant Account](https://docs.adyen.com/account/account-structure)
  - [HMAC Key](https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures)

```bash
export ADYEN_API_KEY="your_adyen_api_key"
export ADYEN_CLIENT_KEY="your_adyen_client_key"
export ADYEN_MERCHANT_ACCOUNT="your_adyen_merchant_account"
export ADYEN_HMAC_KEY="your_adyen_hmac_key"
```

4. Configure allowed origins (CORS)
- It is required to specify the domain or URL of the web applications that will make requests to Adyen. In the Customer Area, add `http://localhost:8080` in the list of Allowed Origins associated with the Client Key.

5. Run `./start.sh` to:
   - Initialize the required environment variables. This step is necessary every time you re-activate your venv
   - Start Python app

6. Visit [http://localhost:8080/](http://localhost:8080/) and select an integration type.

To try out integrations with test card numbers and payment method details, see [Test card numbers](https://docs.adyen.com/development-resources/test-cards/test-card-numbers).


# Webhooks

Webhooks deliver asynchronous notifications about the payment status and other events that are important to receive and process. 

You can find more information about webhooks in [this blog post](https://www.adyen.com/blog/Integrating-webhooks-notifications-with-Adyen-Checkout).

### Webhook setup

In the Customer Area under the `Developers → Webhooks` section, [create](https://docs.adyen.com/development-resources/webhooks/#set-up-webhooks-in-your-customer-area) a new `Standard webhook`.

A good practice is to set up basic authentication, copy the generated HMAC Key and set it as an environment variable. The application will use this to verify the [HMAC signatures](https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures/).

Make sure the webhook is **enabled**, so it can receive notifications.

### Expose an endpoint

This demo provides a simple webhook implementation exposed at `/api/webhooks/notifications` that shows you how to receive, validate and consume the webhook payload.

### Test your webhook

The following webhooks `events` should be enabled:

* **AUTHORISATION**

To make sure that the Adyen platform can reach your application, we have written a [Webhooks Testing Guide](https://github.com/adyen-examples/.github/blob/main/pages/webhooks-testing.md) that explores several options on how you can easily achieve this (e.g. running on localhost or cloud).

## Contributing

We commit all our new features directly into our GitHub repository. Feel free to request or suggest new features or code changes yourself as well!

Find out more in our [Contributing](https://github.com/adyen-examples/.github/blob/main/CONTRIBUTING.md) guidelines.

## License

MIT license. For more information, see the **LICENSE** file in the root directory.