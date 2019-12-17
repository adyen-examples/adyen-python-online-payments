
const checkout = createAdyenCheckout();

const card = checkout
    .create('card', {
        showPayButton: true,
        // groupTypes: ["mc", "visa"]
        // hideCVC: true
        // placeholders: {
        //     encryptedCardNumber: 1111111111111111
        // }

    }).mount('#card');


