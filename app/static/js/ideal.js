const checkout = createAdyenCheckout();

// 2. Create and mount the Component
const card = checkout
    .create('ideal', {
        // showImage: false,
        // issuer: "0031"
        showPayButton: true

    }).mount('#ideal');


