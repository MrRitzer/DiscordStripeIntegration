from flask import Flask, jsonify, request
import json
import requests
import stripe

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = None

with open("token.json", "r") as f:
    js = json.load(f)
    stripe.api_key = js["STRIPE_API_KEY"]
    endpoint_secret = js['STRIPE_ENDPOINT_SECRET']

app = Flask(__name__)

DISCORD_BOT_API_URL = 'http://localhost:5000'  # URL to your running discord_bot.py

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        username = str(event.data.object['custom_fields'])
        print("Username: " + username)
    # ... handle other event types
    else:
    #   print('Unhandled event type {}'.format(event['type']))
        pass

    print(jsonify(success=True))

    return jsonify(success=True)

def handle_invoice_paid(invoice):
    # Assuming the Discord user ID is stored in the metadata of the invoice
    discord_user_id = invoice['metadata'].get('discord_user_id')
    if discord_user_id:
        update_discord_role(discord_user_id)

def update_discord_role(user_id):
    # Send a request to your Discord bot to update the user's role
    try:
        response = requests.post(f'{DISCORD_BOT_API_URL}/update_role', json={'user_id': user_id})
        if response.status_code == 200:
            print("Discord role update request sent successfully")
        else:
            print("Failed to send role update request")
    except Exception as e:
        print(f"Error sending request: {e}")

if __name__ == '__main__':
    app.run(host='localhost', port=4242, debug=True)