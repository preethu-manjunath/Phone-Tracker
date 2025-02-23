from flask import Flask, request, jsonify
import requests
from twilio.rest import Client
from pyicloud import PyiCloudService

app = Flask(__name__)

# Twilio Credentials (Test Only)
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH = "your_twilio_auth"
TWILIO_PHONE = "your_twilio_phone"

def send_alert(phone_number, message):
    """ Sends an emergency SMS alert """
    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE,
        body=message
    )

def get_iphone_location(email, password):
    """ Fetches the last known location of an iPhone using iCloud """
    api = PyiCloudService(email, password)
    devices = api.devices
    return {device.name: device.location for device in devices}

@app.route('/track/iphone', methods=['POST'])
def track_iphone():
    """ API endpoint to track an iPhone """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    location = get_iphone_location(email, password)
    return jsonify({"location": location})

@app.route('/send-alert', methods=['POST'])
def send_sms_alert():
    """ API endpoint to send an emergency alert """
    data = request.json
    phone_number = data.get("phone_number")
    message = data.get("message")
    
    send_alert(phone_number, message)
    return jsonify({"status": "Alert Sent"})

if __name__ == '__main__':
    app.run(debug=True)