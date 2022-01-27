from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from random import randint
import datetime
from cms.viewsUtil import modifySession
from cms.models import *
from cms.forms import updateContact
from cmsUtils.mail import sendEmail
from cmsUtils.sms import sendSMS

user = "pranshu: 12, user_test: user1 "

stuff = dict()

OTP = dict()

stuff['change'] = False

stuff['slots'] = [
    '09:00 AM',
    '09:30 AM',
    '10:00 AM',
    '10:30 AM',
    '11:00 AM',
    '11:30 AM'
]

body = """
Dear Customer,

Thank you for being associated with Clinic Management System (CMS).

You have requested for password change for which One Time Password (OTP):- {} has been generated at {}.

In case you have not requested for password change you can write an email at "noreply.services.2001@gmail.com".

Disclaimer

We recommend you do not share this with anyone to prevent fraudulent transactions.

Sincerely,
Clinic Management System (CMS)
    """


def error(request, path):
    return render(request, 'cms/forbid.html')


def home(request):

    global stuff

    print("home")

    if request.user.is_authenticated == True:

        print(request.user)

        modifySession(request)

        stuff['fresh-login'] = True

        # return render(request, 'cms/profile.html', stuff)
        return redirect('profile')

    return render(request, 'cms/index.html', stuff)


def aboutme(request):

    global stuff

    return render(request, 'cms/about.html', stuff)


def profile(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        stuff['contact'] = Contact.objects.get(user=request.user)
        stuff['age'] = age(to_date(str(stuff['contact'].dob)))

        if request.method == "POST":

            check = updateContact(request.POST, request.FILES, instance=stuff['contact'])
            if check.is_valid():
                
                check.save()
                stuff['warning'] = False
                messages.info(request, "  User Profile Updated Successfully")
            
            else:

                stuff['warning'] = True
                messages.info(request, "  User Profile Update Failed")

        else:

            fresh = stuff.get("fresh-login", False)

            if fresh:

                messages.info(request, "  logged in")
                stuff['warning'] = False
                stuff['fresh-login'] = False

            else:
                stuff['show'] = False
        
        form = updateContact(instance=stuff['contact'])
        stuff['form'] = form

        return render(request, 'cms/profile.html', stuff)

    return redirect('login')


def pastconsult(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        contact = Contact.objects.get(user=request.user)

        stuff['records'] = Details.objects.filter(contact=contact)

        return render(request, 'cms/pastconsult.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def dashboard(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        contact = Contact.objects.get(user=request.user)

        return render(request, 'cms/dashboard.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def pastbooking(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        check_bookings(datetime.date.today())

        stuff['bookings'] = History.objects.filter(patient_id=request.user.id)

        stuff['page'] = "Past Appointments"

        stuff['line'] = "All your past appointments"

        return render(request, 'cms/active_or_pastbooking.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def activebooking(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        check_bookings(datetime.date.today())

        contact = Contact.objects.get(user_id=request.user.id)

        stuff['bookings'] = Booking.objects.filter(contact=contact)
        print(stuff)

        stuff['page'] = "Active Appointments"

        stuff['line'] = "All your pending or active appointments"

        if request.method == "POST":

            checks = request.POST.getlist('book_no')

            if len(checks) > 0:
                for check in checks:
                    res = cancel_booking(check)
                if res != "oops":
                    stuff['warning'] = False
                    if len(checks) == 1:
                        messages.info(request, " Appointment Canceled")
                    else:
                        messages.info(request, " Appointments Canceled")

            return redirect('dashboard')

        return render(request, 'cms/active_or_pastbooking.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def report(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        contact = Contact.objects.get(user=request.user)

        stuff['reports'] = Reports.objects.filter(contact=contact)

        return render(request, 'cms/reports.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def doctors(request):

    global stuff

    modifySession(request)

    if request.user.is_authenticated == True:

        check_bookings(datetime.date.today())

        doctor = Doctor.objects.all()

        stuff['doctors'] = doctor

        if request.method == 'POST':

            doctor = request.POST['booking']

            stuff['doctor'] = Doctor.objects.get(id=doctor)

            return redirect('booking')

        return render(request, 'cms/doctors.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def booking(request):

    modifySession(request)

    if request.user.is_authenticated == True:

        doc = stuff.get('doctor', None)

        if doc == None:

            return redirect('doctors')

        if request.method == 'POST':

            date = request.POST['date']
            slot = request.POST['slot']
            print("date", date, ", Slot-", slot)

            result = has_duplicate(date, slot, stuff['doctor'].id, request.user.id)

            if result != None:

                if result == "Doc":
                    messages.info(request, "  This Slot Is Not Available!")
                else:
                    messages.info(
                        request, "  You Already Have An Appointment In This Slot And Date!")

                stuff['warning'] = True

                return render(request, 'cms/booking.html', stuff)

            stuff['warning'] = False

            messages.info(request, "  Slot Booked")

            booking = Booking()

            contact = Contact.objects.get(user_id=request.user.id)

            doctor = Doctor.objects.get(id=stuff['doctor'].id)

            booking.make_booking(contact, doctor, to_date(date), slot)

            booking.save()

            print(booking)

            print(stuff)

            # render(request, 'booking.html', stuff)
            return redirect('doctors')

        return render(request, 'cms/booking.html', stuff)

    return render(request, 'cms/forbid.html', stuff)


def login(request):

    global stuff

    if request.method == 'POST':

        name = request.POST['name']

        email = request.POST['email']

        password = request.POST['password']

        print(email, password)

        user = auth.authenticate(username=name+"_"+email, password=password)

        if user == None:

            messages.info(request, '  Invalid Login Details')

            stuff['warning'] = True

            return redirect('login')

        else:

            auth.login(request, user)

            request.session["user"] = user.id

            stuff["show"] = True

            stuff['warning'] = False

            print(stuff, messages.get_messages(request=request))

            return redirect('home')

    else:

        return render(request, 'cms/login.html', stuff)


def register(request):

    global stuff

    if request.method == 'POST':

        name = request.POST['name']

        email = request.POST['email']

        gender = request.POST['gender']

        dob = request.POST['dob']

        phone = request.POST['contact']

        address = request.POST['address']

        password = request.POST['password']

        confirm = request.POST['confirm']

        print(dob, gender)

        dob = to_date(dob)

        print(age(dob), gender)

        if password != confirm:

            messages.info(request, '  Password does not match')

            stuff['warning'] = True

            return redirect('register')

        if User.objects.filter(email=email).exists():

            messages.info(request, '  User Exists')

            stuff['warning'] = True

            return redirect('register')

        user = User.objects.create_user(
            username=name+"_"+email, password=password, email=email, first_name=name)
        # user.save()
        contact = Contact()
        contact.make_contact(user, gender, dob, address, phone)
        contact.save()
        messages.info(request, '  User Registered')

        stuff['warning'] = False

        return redirect("login")

    else:
        return render(request, 'cms/register.html', stuff)


def otp(request, uid=-1):

    global stuff, OTP

    print("uid =", uid)

    if request.method == 'POST':

        modifySession(request)

        print(OTP)

        if OTP[uid] == request.POST['otp']:

            messages.info(request, '  Correct OTP')

            stuff['warning'] = False

            stuff['change'] = True

            return redirect('change', uid=uid)
        else:

            messages.info(request, '  Invalid - OTP')

            stuff['warning'] = True

            return render(request, 'cms/otp.html', stuff)

    return render(request, 'cms/otp.html', stuff)


def forgot(request):

    global stuff, OTP, body

    if request.method == "POST":

        email = request.POST['email']

        phone = request.POST['contact']

        try:

            if len(email) > 1:

                user = User.objects.get(email=email)

            else:

                con = Contact.objects.get(phone=phone)

        except:
            messages.info(request, '  User not found!')

            stuff['warning'] = True

            return render(request, 'cms/forgot.html', stuff)

        otp_otp = str(randint(100000, 999999))

        body = body.format(otp_otp, str(datetime.datetime.now()).split(".")[0])

        if len(email) > 1:

            print("Email - ", user.email)
            sendEmail("OTP", otp_otp, email)
            messages.info(
                request, '  An OTP is sent to your regietered email id. ')
            uid = user.id
            OTP[uid] = otp_otp

        else:

            print("SMS - ", con.phone)
            msg = sendSMS(body=body, to="+91"+con.phone)
            messages.info(request, msg)

            if 'fail' in msg:
                stuff['warning'] = True
                return render(request, 'cms/forgot.html', stuff)

            uid = con.user_id
            OTP[uid] = otp_otp

        print(otp_otp)

        stuff['warning'] = False

        return redirect('otp', uid=uid)

    return render(request, 'cms/forgot.html', stuff)


def change(request, uid=-1):

    global stuff

    if stuff['change'] == True:

        stuff['change'] = False

        user = User.objects.get(id=uid)

        stuff['name'] = user.first_name

        return render(request, 'cms/change.html', stuff)

    if request.method == "POST":

        passw = request.POST['password']

        confirm = request.POST['confirm']

        if passw != confirm:

            messages.info(request, '  Password does not match')

            stuff['warning'] = True

            return render(request, 'cms/change.html', stuff)

        user = User.objects.get(pk=uid)

        user.set_password(passw)

        user.save()

        messages.info(request, '  Password is changed')

        stuff['warning'] = False

        return redirect('login')

    return render(request, 'cms/forbid.html', stuff)


def logout(request):

    global stuff

    auth.logout(request)

    messages.info(request, '  User Logged Out ')

    stuff['warning'] = False

    return redirect('home')
