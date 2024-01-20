from flask import Flask, request
import json
import requests

app = Flask(__name__)

DISCORD_BOT_API_URL = 'http://localhost:5000'  # URL to your running discord_bot.py

@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    print("Webhook received with data:", data)

    # Example handling for a subscription payment event
    if data['type'] == 'invoice.paid':
        handle_invoice_paid(data['data']['object'])

    return "Webhook received", 200

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
    app.run(debug=True)