import logging

from Adyen.util import is_valid_hmac_notification
from flask import Flask, render_template, send_from_directory, request, abort

from main.sessions import adyen_sessions
from main.config import *


def create_app():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    app = Flask('app')

    # Register 404 handler
    app.register_error_handler(404, page_not_found)

    # Routes:
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/cart/<integration>')
    def cart(integration):
        return render_template('cart.html', method=integration)

    @app.route('/checkout/<integration>')
    def checkout(integration):

        if integration in get_supported_integration():
            return render_template('component.html', method=integration, client_key=get_adyen_client_key())
        else:
            abort(404)

    @app.route('/api/sessions', methods=['POST'])
    def sessions():
        host_url = request.host_url 

        return adyen_sessions(host_url)

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

        return render_template('component.html', method=None, client_key=get_adyen_client_key())

    # Process incoming webhook notifications
    @app.route('/api/webhooks/notifications', methods=['POST'])
    def webhook_notifications():
        """
        Receives outcome of each payment
        :return:
        """
        notifications = request.json['notificationItems']
        # fetch first( and only) NotificationRequestItem
        notification = notifications[0]

        if is_valid_hmac_notification(notification['NotificationRequestItem'], get_adyen_hmac_key()) :
            # consume event asynchronously
            consume_event(notification)
        else:
            # invalid hmac: do not send [accepted] response
            raise Exception("Invalid HMAC signature")

        return '', 202

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'img/favicon.ico')

    return app


#  process payload asynchronously
def consume_event(notification):
    print(f"consume_event merchantReference: {notification['NotificationRequestItem']['merchantReference']} "
          f"result? {notification['NotificationRequestItem']['success']}")

    # add item to DB, queue or run in a different thread


def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    web_app = create_app()

    logging.info(f"Running on http://localhost:{get_port()}")
    web_app.run(debug=True, port=get_port(), host='0.0.0.0')


