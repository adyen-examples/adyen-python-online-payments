const checkout = createAdyenCheckout();

const dropin = checkout
    .create('dropin', {
        paymentMethodsConfiguration: {
            // applepay: { //Example configuration
            //     configuration: { //Required configuration for Apple Pay
            //         merchantName: 'TylerDouglas', // Name to be displayed on the form
            //         merchantIdentifier: '01234567890' // Your Apple merchant identifier as described https://developer.apple.com/documentation/apple_pay_on_the_web/applepayrequest/2951611-merchantidentifier
            //     },
            // },
            card: { //Example optional configuration for Cards
                // hasHolderName: true,
                // holderNameRequired: true,
                enableStoreDetails: true,
                name: 'Credit or debit card',
                placeholders: {
                    encryptedCardNumber: "",
                    encryptedSecurityCode: ""
                }
            }
        },

    }).mount('#dropin');

