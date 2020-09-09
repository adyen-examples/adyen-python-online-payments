// Structure credit card payment request
const structureRequest = (data) => {

    const paymentRequest = {
        paymentMethod: data.paymentMethod
    };

    if (data.paymentMethod.type === "scheme") {
        paymentRequest['billingAddress'] = data.billingAddress;
        paymentRequest['browserInfo'] = data.browserInfo;
    }

    return paymentRequest;
};

// Parse payment response and directing shopper to correct place
const handleFinalState = (resultCode) => {
    if (resultCode === 'Authorised') {
        window.location.href = "http://localhost:8080/success";

    } else if (resultCode === 'Pending' || resultCode === 'Received') {
        window.location.href = "http://localhost:8080/pending";

    } else if (resultCode === 'Error') {
        window.location.href = "http://localhost:8080/error";

    } else {
        window.location.href = "http://localhost:8080/failed";
    }
};

/*
 * Dropin and Component event handlers
 *
 * And Create Adyen checkout method
 */

const onSubmit = (state, component) => {
    fetch(`/api/initiatePayment`, {
        method: 'POST',
        headers: {
            Accept: 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(structureRequest(state.data))
    }).then(response => response.json())
        .then(response => {
            if (response.action) {
                if (response.resultCode === 'RedirectShopper') {
                    localStorage.setItem('redirectPaymentData', response.action.paymentData);
                }
                adyenComponent.handleAction(response.action);

            } else {
                handleFinalState(response.resultCode);
            }
        })
        .catch(error => {
            console.log(error);
            window.location.href = "http://localhost:8080/failed";
        });
};

const onAdditionalDetails = (state, component) => {
    console.log("OnAdditionalDetails triggered");
    fetch(`/api/submitAdditionalDetails`, {
        method: 'POST',
        headers: {
            Accept: 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(state.data)
    }).then(response => response.json())
        .then(response => {
            if (response.action) {
                adyenComponent.handleAction(response.action);
            } else {
                handleFinalState(response.resultCode);
            }
        })
        .catch(error => {
            console.log(error);
            window.location.href = "http://localhost:8080/failed";
        });
};

const onError = (error) => {
    console.log(error);
};


// Create Adyen checkout instance and initilize component
const createAdyenCheckout = () => {
    // Get /paymentMethods call and clientKey response Jinja2 passed back to <script> tag
    const paymentMethods = JSON.parse(document.getElementById('payment-methods').innerHTML);
    const clientKey = JSON.parse(document.getElementById('client-key').innerHTML);

    // Docs for custom styling of dropin - https://docs.adyen.com/checkout/drop-in-web/customization
    // Docs for configuration changes to components (configurations are payment method specific) E.g. Cards - https://docs.adyen.com/payment-methods/cards/web-component#show-the-available-cards-in-your-payment-form
    const paymentMethodsConfiguration = {
        card: {
            hasHolderName: true,
            holderNameRequired: true,
            enableStoreDetails: true,
        },
        ach: {
            holderName: 'Ach User',
            billingAddressRequired: false
        },
        paypal: {
            amount: {
                currency: "USD",
                value: 1000
            },
            environment: "test", // Change this to "live" when you're ready to accept live PayPal payments
            countryCode: "US", // Only needed for test. This will be automatically retrieved when you are in production.
            intent: "authorize", // Change this to "authorize" if the payments should not be captured immediately. Contact Support to enable this flow.
        }
    };

    const configObj = {
        paymentMethodsConfiguration: paymentMethodsConfiguration,
        showPayButton: true,
        locale: "en_US",
        environment: "test",
        clientKey: clientKey,
        paymentMethodsResponse: paymentMethods,
        onSubmit: onSubmit,
        onAdditionalDetails: onAdditionalDetails,
        onError: onError
    };
    return new AdyenCheckout(configObj);
};
const integrationType = JSON.parse(document.getElementById('integration-type').innerHTML);

// Adjust style for Specific Components
if (integrationType === 'dropin') {
    document.getElementById('component').style.padding = '0em';
    let container = document.getElementsByClassName('checkout-component')[0];
    container.style.border = 'none';
    container.style.padding = '0';
} else if (integrationType === 'paypal') {
    let el = document.querySelector('.payment');
    el.style.display = 'flex';
    el.style.justifyContent = 'center';
}

const checkout = createAdyenCheckout();
const adyenComponent = checkout.create(integrationType).mount("#component");

