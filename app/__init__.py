import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, abort

from .main.config import read_config
from .main.payments import adyen_payments
from .main.payment_methods import adyen_payment_methods
from .main.redirect import handle_shopper_redirect
from .main.additional_details import get_payment_details
import app.main.config as config


# Fusion Application Factory
def create_app():
    app = Flask('app')

    # Register 404 handler
    app.register_error_handler(404, page_not_found)

    # read in values from config.ini file and load them into project
    read_config()

    # Routes:
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/cart/<integration>')
    def cart(integration):
        return render_template('cart.html', method=integration)

    @app.route('/checkout/<integration>')
    def checkout(integration):
        payment_methods_response = adyen_payment_methods()
        client_key = config.client_key

        if integration in config.supported_integrations:
            return render_template('component.html', method=integration, payment_methods=payment_methods_response,
                                   client_key=client_key)
        else:
            abort(404)

    @app.route('/api/getPaymentMethods', methods=['GET'])
    def get_payment_methods():
        payment_methods_response = adyen_payment_methods()
        return payment_methods_response

    @app.route('/api/initiatePayment', methods=['POST'])
    def initiate_payment():
        payment_response = adyen_payments(request)
        return payment_response

    @app.route('/api/submitAdditionalDetails', methods=['POST'])
    def payment_details():
        details_response = get_payment_details(request)
        return details_response

    @app.route('/api/handleShopperRedirect', methods=['POST', 'GET'])
    def handle_redirect():
        values = request.json if request.is_json else request.values.to_dict()  # Get values from request object

        # Fetch paymentData from the frontend if we have not already
        if 'paymentData' in values:
            redirect_response = handle_shopper_redirect(values)
            if redirect_response["resultCode"] == 'Authorised':
                return redirect(url_for('checkout_success'))
            elif redirect_response["resultCode"] == 'Received' or redirect_response["resultCode"] == 'Pending':
                return redirect(url_for('checkout_pending'))
            else:
                return redirect(url_for('checkout_failure'))
        else:
            return render_template('fetch-payment-data.html', values=values)

    @app.route('/result/success', methods=['GET'])
    def checkout_success():
        return render_template('checkout-success.html')

    @app.route('/result/failed', methods=['GET'])
    def checkout_failure():
        return render_template('checkout-failed.html')

    @app.route('/result/pending', methods=['GET'])
    def checkout_pending():
        return render_template('checkout-success.html')

    @app.route('/result/error', methods=['GET'])
    def checkout_error():
        return render_template('checkout-failed.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'img/favicon.ico')

    return app


def page_not_found(error):
    return render_template('error.html'), 404
