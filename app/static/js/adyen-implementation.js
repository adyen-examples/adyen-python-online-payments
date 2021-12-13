const clientKey = JSON.parse(document.getElementById('client-key').innerHTML);
const type = JSON.parse(document.getElementById('integration-type').innerHTML);

async function initCheckout() {
	try {
		const checkoutSessionResponse = await callServer("/api/sessions?type=" + type);

		const configuration = {
			clientKey,
			locale: "en_US",
			environment: "test", // Change this to "live" on production
			showPayButton: true,
			session: checkoutSessionResponse,
			paymentMethodsConfiguration: {
				ideal: {
					showImage: true
				},
				card: {
					hasHolderName: true,
					holderNameRequired: true,
					name: "Credit or debit card",
					amount: {
						value: 1000,
						currency: "EUR"
					}
				},
				paypal: {
					amount: {
						currency: "USD",
						value: 1000
					},
					environment: "test", // Change this to "live" when you're ready to accept live PayPal payments
					countryCode: "US"   // Only needed for test. This will be automatically retrieved when you are in production.
				}
			},
			onPaymentCompleted: (result, component) => {
				console.log(result, console);
			},
			onError: (error, component) => {
				console.error(error.name, error.message, error.stack, component);
			}
		};

        // Create an instance of AdyenCheckout using the configuration object.
		const checkout = await new AdyenCheckout(configuration);

		// Create an instance of Drop-in and mount it to the container you created.
		const dropinComponent = checkout.create(type).mount("#component");  // pass DIV id where component must be rendered

	} catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	}
}


// Event handlers called when the shopper selects the pay button,
// or when additional information is required to complete the payment
async function handleSubmission(state, component, url) {
	try {
		const res = await callServer(url, state.data);
		handleServerResponse(res, component);
	} catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	}
}

// Calls your server endpoints
async function callServer(url, data) {
	const res = await fetch(url, {
		method: "POST",
		body: data ? JSON.stringify(data) : "",
		headers: {
			"Content-Type": "application/json"
		}
	});

	return await res.json();
}

// Handles responses sent from your server to the client
function handleServerResponse(res, component) {
	if (res.action) {
		component.handleAction(res.action);
	} else {
		switch (res.resultCode) {
			case "Authorised":
				window.location.href = "/result/success";
				break;
			case "Pending":
			case "Received":
				window.location.href = "/result/pending";
				break;
			case "Refused":
				window.location.href = "/result/failed";
				break;
			default:
				window.location.href = "/result/error";
				break;
		}
	}
}

initCheckout();
