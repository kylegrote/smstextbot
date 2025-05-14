import os
from twilio.rest import Client


def formatPhoneNumber(phoneNumber, countryCode="1"):
    if type(phoneNumber) == int:
        if str(phoneNumber)[0] == f"{countryCode}":
            formatedPhoneNumber = f"+{phoneNumber}"
        else:
            formatedPhoneNumber = f"+{countryCode}{phoneNumber}"
    elif type(phoneNumber) == str:
        phoneNumber = ''.join([char for char in phoneNumber if char.isdigit() == True])
        if phoneNumber[0] == countryCode:
            formatedPhoneNumber = f"+{phoneNumber}"
        else:
            formatedPhoneNumber = f"+{countryCode}{phoneNumber}"

    return formatedPhoneNumber

def sendSMS(phoneNumber, message, countryCode="1"):
   # <------------------------------connect to twilio and send an sms------------------>
   twilioAccountSid = os.getenv("twilioAccountSid")
   twilioAuthToken = os.getenv("twilioAuthToken")
   client = Client(twilioAccountSid, twilioAuthToken)
   message = client.messages.create(
       body=message,
       from_="+12532158111",
       to=f"{formatPhoneNumber(phoneNumber)}",
   )


def TESTsendSMS(phoneNumber, message, countryCode="1"):
    print(f"phone:{phoneNumber}\nmessage:\n{message}")






