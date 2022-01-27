# from django.shortcuts import redirect
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from io import BytesIO
from random import randint

# importing stuff from cms module which is parallel to cms_api(this) module
from cms.models import *
# , UserSerializer
from cms.serializers import ContactSerializer, HistorySerializer, DoctorSerializer

# importing stuff from cmsUtils module which is parallel to cms_api(this) module
from cmsUtils.apiUtils import models_to_dict, get_contact_or_none, validate_signup
from cmsUtils.mail import sendEmail
from cmsUtils.sms import sendSMS

# sms and mail body string
from cms.views import body#, booking, stuff
# Create your views here.

instructions = "api-endpoint http://127.0.0.1:8000/cms-api-signup for user registeration (username, password, gender(m/f), dob, address, phone) "

api_list = [
    "http://127.0.0.1:8000/cms-api/patient/",
    "http://127.0.0.1:8000/cms-api/doctor/",
    "http://127.0.0.1:8000/cms-api/history/",
    "http://127.0.0.1:8000/cms-api/details/",
    "http://127.0.0.1:8000/cms-api/reports/",
    "http://127.0.0.1:8000/cms-api/booking/",
    "http://127.0.0.1:8000/cms-api/history/",
    "http://127.0.0.1:8000/cms-api/api-get-otp/",
    "http://127.0.0.1:8000/cms-api/help/",
]


def instruction(request):
    return JsonResponse({"MSG": instructions, "API-List": api_list}, safe=False)


@csrf_exempt
def signup(request):

    try:

        if len(request.body) > 0:

            python_data = JSONParser().parse(BytesIO(request.body))
            print(python_data)
            valid = validate_signup(python_data)
            print(valid)

            if valid != None:

                return JsonResponse({"ERR": valid}, safe=False)

            print(python_data)
            ser = ContactSerializer(data=python_data)

            if ser.is_valid():
                ser.save()
                print("Data Saved")
                return JsonResponse({"MSG": "DATA SAVED", "DATA": ser.data}, safe=False)

            return JsonResponse({"ERR": ser.errors}, safe=False)

        else:

            return JsonResponse({"ERR": "Empty Json File, use these '{' '}' "}, safe=False)

    except Exception as error:

        print("Exception", error)
        return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class request_otp(APIView):

    def serve(sef, request):

        global body

        try:

            if len(request.body) > 0:

                try:
                    email = JSONParser().parse(BytesIO(request.body)).pop("email")
                    sms = JSONParser().parse(BytesIO(request.body)).pop("sms")
                except Exception as ex:
                    print("[SERVER-ERROR]", ex)
                    return JsonResponse({"ERR": "email or sms not provided!"}, safe=False)

                # genrating a 6-digit random OTP for validation
                otp = str(randint(100000, 999999))
                body = body.format(
                    otp, str(datetime.datetime.now()).split(".")[0])

                if email != "":

                    sendEmail(subject="OTP", body=body, to=email)
                    msg = "Email."

                elif sms != "":

                    res = sendSMS(body=body, to=sms)
                    if "fail" in res:
                        return JsonResponse({"ERR": "phone number is not in the correct format i.e '+91<phone number>'."}, safe=False)
                    msg = "Mobile Number."

                else:
                    return JsonResponse({"ERR": "either 'email' or 'phone number' is required but both not provided! please provide one."}, safe=False)

                return JsonResponse({"MSG": "OTP Sent To The Registered "+msg, "OTP": otp}, safe=False)

            else:

                return JsonResponse({"ERR": "Empty Json File, put these '{' '}' "}, safe=False)

        except Exception as error:

            print("[SERVER-ERROR]", error)
            return JsonResponse({"ERR": error}, safe=False)

    def get(self, request):

        return self.serve(request)

    def post(self, request):

        return self.serve(request)


@method_decorator(csrf_exempt, name="dispatch")
class patient_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            # print(len(request.body))
            if len(request.body) > 0:
                try:

                    ct = Contact.objects.get(user_id=request.user.id)
                    data = ContactSerializer(ct).data.copy()
                    data["age"] = age(to_date(str(ct.dob)))
                    print(data)
                    return JsonResponse(data, safe=False)

                except:

                    return JsonResponse({"ERR": "Id Does Not Exist"}, safe=False)

            else:

                return JsonResponse({"ERR": "Empty Json File, put these '{' '}' "}, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class doctor_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            if len(request.body) > 0:

                check_bookings(datetime.date.today())
                python_data = JSONParser().parse(BytesIO(request.body))

                if "doctor_id" in python_data.keys():

                    try:

                        doc = Doctor.objects.get(
                            id=python_data.pop("doctor_id"))
                        ser = DoctorSerializer(doc)
                        return JsonResponse(ser.data, safe=False)

                    except:

                        return JsonResponse({"ERR": "ID Does Not Exist"}, safe=False)

                else:

                    doc = Doctor.objects.all()
                    ser = DoctorSerializer(doc, many=True)
                    return JsonResponse(ser.data, safe=False)

            else:

                return JsonResponse({"ERR": "Empty Json File, put these '{' '}' "}, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class history_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            if len(request.body) > 0:

                try:

                    print("User", request.user.id)
                    his = History.objects.filter(patient_id=request.user.id)
                    ser = HistorySerializer(his, many=True)
                    return JsonResponse(ser.data, safe=False)

                except Exception as error:

                    print("[SERVER-ERROR]", error)
                    return JsonResponse({"ERR": "User Does Not Exist!"}, safe=False)

            else:

                return JsonResponse({"ERR": "Empty Json File, put these '{' '}' "}, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class details_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            contact = get_contact_or_none(Contact.objects, request.user.id)

            if contact == None:
                print("[SERVER-ERROR] Id Does not Exist")
                return JsonResponse({"ERR": "ID Does Not Exist"}, safe=False)

            details = Details.objects.filter(contact_id=contact.id)
            data = models_to_dict(details)
            print("json-data:\n", data)
            return JsonResponse(data, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class reports_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            contact = get_contact_or_none(Contact.objects, request.user.id)

            if contact == None:
                msg = "Id Does not Exist"
                print("[SERVER-ERROR]", msg)
                return JsonResponse({"ERR": msg}, safe=False)

            reports = Reports.objects.filter(contact_id=contact.id)
            data = models_to_dict(reports, report=True)
            print("json-data:\n", data)
            return JsonResponse(data, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class booking_api(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            contact = get_contact_or_none(Contact.objects, request.user.id)

            if contact == None:
                msg = "User Does Not Exist!"
                print("[SERVER-MSG]", msg)
                return JsonResponse({"ERR": msg}, safe=False)

            bookings = Booking.objects.filter(contact_id=contact.id)
            data = models_to_dict(bookings)
            print("json-data:\n", data)
            return JsonResponse(data, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)

    def post(self, request):

        data=""
        try:

            python_data = JSONParser().parse(BytesIO(request.body))
            print("Data Recieved", python_data)

            try:

                date = python_data.pop("date")
                slot = python_data.pop("slot")
                doc_id = python_data.pop("doc_id")

            except Exception as error:

                print("[SERVER-ERROR]", error)
                return JsonResponse({"ERR": " Either date or slot or doctor_id is not given!"}, safe=False)

            result = has_duplicate(date, slot, doc_id, request.user.id)
            print(request.user.id)
            if result != None:

                if result == "Doc":
                    msg = " This Slot Is Not Available!"
                else:
                    msg = " You Already Have An Appointment In This Slot And Date!"
            else:

                booking = Booking()
                booking.make_booking(Contact.objects.get(user_id=request.user.id), Doctor.objects.get(id=doc_id), to_date(date), slot)
                booking.save()
                data = booking.get_dict()
                msg = " Slot Booked!"

            print("json-data:\n", msg)
            return JsonResponse({"MSG": msg, "data": data}, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)

    def delete(self, request):

        try:

            python_data = JSONParser().parse(BytesIO(request.body))
            print("Data Recieved", python_data)

            if "booking-ids" in python_data.keys():

                res = ""
                for bookings in python_data["booking-ids"]:
                    res += cancel_booking(bookings)+" "

                if "oops" not in res:

                    if len(python_data["booking-ids"]) == 1:
                        msg = " Appointment Canceled"
                    else:
                        msg = " Appointments Canceled"

                else:
                    msg = "[SERVER-ERROR] booking id does not exist!"

                print("json-data:\n", msg)
                return JsonResponse({"MSG": msg}, safe=False)

            else:

                msg = "booking-ids are required but not provided"
                print("Error -", msg)
                return JsonResponse({"ERR": msg}, safe=False)

        except Exception as error:

            print("Exception", error)
            return JsonResponse({"ERR": error}, safe=False)
