import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, abort

from .main.config import read_config
from .main.payments import initiate_payment
from .main.payment_methods import get_payment_methods
from .main.redirect import handle_shopper_redirect
from .main.additional_details import get_payment_details
import app.main.config as config


# Fusion Application Factory
def create_app():
    app = Flask('fusion')

    # Update root_path to specific module. If using multiple modules, can define relative to instance path
    app.root_path = app.root_path + '/app'

    # Register 404 handler
    app.register_error_handler(404, page_not_found)

    # read in values from config.ini file and load them into project
    read_config()

    # Routes:
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/<integration>/cart')
    def cart(integration):
        return render_template('cart.html', method=integration)

    @app.route('/<integration>/checkout')
    def checkout(integration):
        payment_methods_response = get_payment_methods()
        origin_key = config.origin_key
        if integration == 'dropin':
            return render_template('dropin.html', method=integration, payment_methods=payment_methods_response,
                                   origin_key=origin_key)
        elif integration == 'card':
            return render_template('card.html', method=integration, payment_methods=payment_methods_response,
                                   origin_key=origin_key)
        elif integration == 'ideal':
            return render_template('ideal.html', method=integration, payment_methods=payment_methods_response,
                                   origin_key=origin_key)
        else:
            abort(404)

    @app.route('/initiatePayment', methods=['POST'])
    def init_payments():
        payment_response = initiate_payment(request)
        return payment_response

    @app.route('/submitAdditionalDetails', methods=['POST'])
    def payment_details():
        details_response = get_payment_details(request)
        return details_response

    @app.route('/handleShopperRedirect', methods=['POST', 'GET'])
    def handle_redirect():
        values = request.json if request.is_json else request.values.to_dict()  # Get values from request object

        # Fetch paymentData from the frontend if we have not already
        if 'paymentData' in values:
            redirect_response = handle_shopper_redirect(values)
            if redirect_response["resultCode"] == 'Authorised' or redirect_response["resultCode"] == 'Received':
                return redirect(url_for('checkout_success'))
            else:
                return redirect(url_for('checkout_failure'))
        else:
            return render_template('fetch-payment-data.html', values=values)

    @app.route('/checkout/complete', methods=['GET'])
    def checkout_success():
        return render_template('checkout-complete.html')

    @app.route('/checkout/failed', methods=['GET'])
    def checkout_failure():
        return render_template('checkout-failed.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'img/favicon.ico')

    return app


def page_not_found(error):
    return render_template('error.html'), 404
