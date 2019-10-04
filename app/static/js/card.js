
const checkout = createAdyenCheckout();

const card = checkout
    .create('card', {
        showPayButton: true,
        // placeholders: {
        //     encryptedCardNumber: 1111111111111111
        // }

    }).mount('#card');


