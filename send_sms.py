# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH')
print(auth_token)
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Twilio test",
                     from_='+19844597459',
                     to='+19197375711'
                 )

print(message.sid)