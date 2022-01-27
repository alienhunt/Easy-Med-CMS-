from logging import exception
from os import environ
from twilio.rest import Client

# sendSMS takes two str type objects body and to, if to is not provided then the sms will be sent to the default number
def sendSMS(body, to=environ["MY_PHONE_NUMBER"]):

    try :
        client = Client(environ["TWILIO_ACC_SID"], environ["TWILIO_AUTH_TOKEN"])

        client.messages.create(
            to=to,
            from_=environ["TWILIO_NUMBER"],
            body=body
        )
    except Exception as ex:
        ex = "[SERVER-ERROR] internal server error -{} \nfailed to send sms!".format(ex)
        print(ex)
        return "  [SERVER-ERROR] - failed to send sms!"


    print("SMS SENT!")
    return '  An OTP is sent to your regietered mobile number.'