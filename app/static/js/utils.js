// Get shopper reference
// Should be collected from shopper's profile
const getShopperReference = () => {
    return 'Fusion Shopper Reference';
};


// Get amount of payment and currency
// Should be obtained from cookie passed from previous page
const getAmount = () => {
    return {
        value: 1000,
        currency: 'EUR'
    };
};


// Iterate over form inputs and collect and structure billing address details
const getBillingAddress = () => {
    const inputs = document.getElementById('address').querySelectorAll('input');
    let billingAddress = {};

    // Skipping initial radiobox
    for (let i = 1; i < inputs.length; i++) {
        billingAddress[inputs[i].name] = inputs[i].value;
    }

    // resolve full county to 2 letter country code
    // or you could use 2 letter country code spinner
    billingAddress['country'] = 'US';
    const regex = /\d+/g;
    billingAddress['houseNumberOrName'] = billingAddress['street'].match(regex).map(Number)[0]; //Assumes first #
    billingAddress['street'] = billingAddress['street'].replace(regex, '').trim();

    // console.log(myObject);
    return billingAddress;
};


// Structure credit card payment request
const structurePaymentsRequest = (paymentMethodData, billingAddress) => {
    const dt = new Date();

    paymentMethodData["paymentMethod"]["holderName"] = billingAddress["firstName"].concat(" ", billingAddress["lastName"]);
    delete billingAddress["firstName"];
    delete billingAddress["lastName"];

    const paymentRequest = {
        amount: getAmount(),
        shopperReference: getShopperReference(),
        ...paymentMethodData,
        billingAddress,
        browserInfo: {
            javaEnabled: window.navigator.javaEnabled(),
            colorDepth: screen.colorDepth,
            screenHeight: screen.height,
            screenWidth: screen.width,
            timeZoneOffset: dt.getTimezoneOffset()
        }
    };

    console.log(paymentRequest);
    return paymentRequest;
};


// Structure a /payments request for the iDEAL payment method
const structureIdealPaymentsRequest = (paymentMethodData) => {
    const paymentRequest = {
        amount: getAmount(),
        shopperReference: getShopperReference(),
        ...paymentMethodData
    };

    return paymentRequest;
};


// Parse payment response and directing shopper to correct place
const handleFinalState = (resultCode) => {
    if (resultCode === 'Authorised') {
        window.location.href = "http://localhost:5000/checkout/complete";

    } else {
        window.location.href = "http://localhost:5000/checkout/failed";
    }
};

const stringifyPayment = (data, name) => {
    if (name === 'iDEAL') {
        return structureIdealPaymentsRequest(data);
    } else {
        return structurePaymentsRequest(data, getBillingAddress());
    }
};


/*
 * Dropin and Component event handlers
 *
 * And Create Adyen checkout method
 */

const onSubmit = (state, component) => {
    fetch(`/initiatePayment`, {
        method: 'POST',
        headers: {
            Accept: 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(stringifyPayment(state.data, component.props.name))
    }).then(response => response.json())
        .then(response => {
            if (response.action) {
                if (response.resultCode === 'RedirectShopper') {
                    localStorage.setItem('redirectPaymentData', response.action.paymentData);
                }
                if (component.props.isDropin) {
                    dropin.handleAction(response.action);
                } else {
                    checkout.createFromAction(response.action).mount('#additional-details');
                }
            } else {
                handleFinalState(response.resultCode);
            }
        })
        .catch(error => {
            throw Error(error);
        });
};

const onAdditionalDetails = (state, component) => {
    console.log("On aditional detaiils");
    console.log(state.data);
    fetch(`/submitAdditionalDetails`, {
        method: 'POST',
        headers: {
            Accept: 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },

        body: JSON.stringify(state.data)
    }).then(response => response.json())
        .then(response => {
            if (response.action) {
                if (component.props.isDropin) {
                    dropin.handleAction(response.action);
                } else {
                    checkout.createFromAction(response.action).mount('#additional-details');
                }
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
    throw Error(error);
};


// Create Adyen checkout instance and return it
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


    const configObj = {
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

