from twilio.rest import Client

from decouple import config

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
message = client.messages.create(
  messaging_service_sid='MGf6cbeb77420eb2770cd2b66be77db8f8',
  body='Ahoy 👋',
  to='+919048444482',
)
print(message.sid)