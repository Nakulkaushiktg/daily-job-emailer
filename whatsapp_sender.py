# whatsapp_sender.py
from twilio.rest import Client
import os

def send_whatsapp(message_body):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    from_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox number
    to_whatsapp = "whatsapp:+91XXXXXXXXXX"   # Replace with your real WhatsApp number

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print(f"✅ WhatsApp message sent: {message.sid}")
    except Exception as e:
        print(f"❌ WhatsApp message failed: {e}")
