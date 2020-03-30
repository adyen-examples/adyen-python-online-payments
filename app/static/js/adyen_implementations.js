// Structure credit card payment request
const structureRequest = (data) => {

    const paymentRequest = {
        paymentMethod: data.paymentMethod
    };

    if (data.paymentMethod.type === "scheme") {
        paymentRequest['billingAddress'] = data.billingAddress;
        paymentRequest['browserInfo'] = data.browserInfo;
    }

    console.log(paymentRequest);
    return paymentRequest;
};

// Parse payment response and directing shopper to correct place
const handleFinalState = (resultCode) => {
    if (resultCode === 'Authorised') {
        window.location.href = "http://localhost:5000/success";

    } else if (resultCode === 'Pending') {
        window.location.href = "http://localhost:5000/pending";

    } else if (resultCode === 'Error') {
        window.location.href = "http://localhost:5000/error";

    } else {
        window.location.href = "http://localhost:5000/failed";
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
            window.location.href = "http://localhost:5000/failed";
        });
};

const onAdditionalDetails = (state, component) => {
    console.log("On additionalDetails triggered");
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
            throw Error(error);
        });
};

const onError = (error) => {
    console.log(error);
};


// Create Adyen checkout instance and initilize component
const createAdyenCheckout = () => {
    // Get /paymentMethods call and originKey response Jinja2 passed back to <script> tag
    // Need to run JSON.parse() 2x because Jinja2 |tojson filter stringifies /paymentMethod response again. However,
    // not including this filter results in an HTML encoded string
    const paymentMethods = JSON.parse(JSON.parse(document.getElementById('payment-methods').innerHTML));
    const originKey = JSON.parse(document.getElementById('origin-key').innerHTML);

    // Placeholder values
    const translations = {
        // "en-US": {
        //     "creditCard.numberField.title": "Custom Card Name",
        // }
    };

    const paymentMethodsConfiguration = {
        // applepay: { // Example required configuration for Apple Pay
        //     configuration: {
        //         merchantName: 'Adyen Test merchant', // Name to be displayed on the form
        //         merchantIdentifier: 'adyen.test.merchant' // Your Apple merchant identifier as described in https://developer.apple.com/documentation/apple_pay_on_the_web/applepayrequest/2951611-merchantidentifier
        //     },
        //     onValidateMerchant: (resolve, reject, validationURL) => {
        //         // Call the validation endpoint with validationURL.
        //         // Call resolve(MERCHANTSESSION) or reject() to complete merchant validation.
        //     }
        // },
        // paywithgoogle: { // Example required configuration for Google Pay
        //     environment: "TEST", // Change this to PRODUCTION when you're ready to accept live Google Pay payments
        //     configuration: {
        //         gatewayMerchantId: "TylerDouglas", // Your Adyen merchant or company account name. Remove this field in TEST.
        //         merchantIdentifier: "12345678910111213141" // Required for PRODUCTION. Remove this field in TEST. Your Google Merchant ID as described in https://developers.google.com/pay/api/web/guides/test-and-deploy/deploy-production-environment#obtain-your-merchantID
        //     }
        // },
        card: { // Example optional configuration for Cards
            // hideCVC: false, // Change this to true to hide the CVC field for stored cards. false is default
            // placeholders: { # Change placeholder text for the following fields
            // encryptedCardNumber: "",
            // encryptedSecurityCode: ""
            // },
            // billingAddressRequired: true,
            hasHolderName: true,
            holderNameRequired: true,
            enableStoreDetails: true,
            name: 'Credit or debit card'
        },
        ach: { // Default ACH user information
            holderName: 'Ach User',
            data: {
                billingAddress: {
                    street: 'Infinite Loop',
                    postalCode: '95014',
                    city: 'Cupertino',
                    houseNumberOrName: '1',
                    country: 'US',
                    stateOrProvince: 'CA'
                }
            }
        }
    };

    const configObj = {
        paymentMethodsConfiguration: paymentMethodsConfiguration,
        showPayButton: true,
        locale: "en_US",
        environment: "test",
        originKey: originKey,
        paymentMethodsResponse: paymentMethods,
        translations: translations,
        onSubmit: onSubmit,
        onAdditionalDetails: onAdditionalDetails,
        onError: onError
    };
    return new AdyenCheckout(configObj);
};
const integrationType = JSON.parse(document.getElementById('integration-type').innerHTML);

// Adjust style for Dropin
if (integrationType === 'dropin') {
    document.getElementById('component').style.padding = '0em';
    document.getElementsByClassName('checkout-component')[0].style.border = 'none';
}

const checkout = createAdyenCheckout();
const adyenComponent = checkout.create(integrationType).mount("#component");

