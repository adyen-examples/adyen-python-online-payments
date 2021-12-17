import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, abort

from .main.config import read_config
from .main.redirect import handle_shopper_redirect
import app.main.config as config

from .main.sessions import adyen_sessions


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
        client_key = config.client_key
        platform = config.platform

        if integration in config.supported_integrations:
            return render_template('component.html', method=integration, client_key=client_key, platform=platform)
        else:
            abort(404)

    @app.route('/api/sessions', methods=['POST'])
    def sessions():
        return adyen_sessions()

    @app.route('/api/handleShopperRedirect', methods=['POST', 'GET'])
    def handle_redirect():
        values = request.values.to_dict()  # Get values from query params in request object
        details_request = {}

        if "payload" in values:
            details_request["details"] = {"payload": values["payload"]}
        elif "redirectResult" in values:
            details_request["details"] = {"redirectResult": values["redirectResult"]}

        redirect_response = handle_shopper_redirect(details_request)

        # Redirect shopper to landing page depending on payment success/failure
        if redirect_response["resultCode"] == 'Authorised':
            return redirect(url_for('checkout_success'))
        elif redirect_response["resultCode"] == 'Received' or redirect_response["resultCode"] == 'Pending':
            return redirect(url_for('checkout_pending'))
        else:
            return redirect(url_for('checkout_failure'))

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

    # Handle redirect (required for some payment methods)
    @app.route('/redirect', methods=['POST', 'GET'])
    def redirect():
        client_key = config.client_key
        platform = config.platform

        return render_template('component.html', method=None, client_key=client_key, platform=platform)


    @app.route('/api/webhook/notifications', methods=['POST'])
    def webhook_notifications():
        """
        Receives outcome of each payment
        :return:
        """
        notifications = request.json['notificationItems']

        for notification in notifications:
            print(f"merchantReference: {notification['NotificationRequestItem']['merchantReference']} "
                  f"result? {notification['NotificationRequestItem']['success']}")

        return '[accepted]'

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'img/favicon.ico')

    return app


def page_not_found(error):
    return render_template('error.html'), 404
