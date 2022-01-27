from django.db import models

from django.contrib.auth.models import User

import datetime

# Create your models here.

# The list below contains the names of all the models in this application
# models_list = ["Doctor", "Contact", "Details", "Reports", "Booking", "History"]


def cancel_booking(booking_id):

    try:
        booking = Booking.objects.get(id=booking_id)
    except Exception as ex:
        print("[MODLE_ERROR]", ex)
        return "oops"

    his = History()
    his.add_to_history(booking.id, booking.contact.user.username, booking.doctor.name,
                       booking.contact.user_id, booking.doctor_id, booking.booking_date,  booking.time_slot)
    his.reason = "Canceled"
    his.save()

    booking.delete()
    return ""


def to_date(date):

    if type(date) == str:
        date = date.replace(" ", "")
        date = list(map(int, date.split("-")))
        date = datetime.date(date[0], date[1], date[2])

    return date


def has_duplicate(date, slot, doctor_id, patient_id):

    booking = Booking.objects.filter(doctor_id=doctor_id)

    if type(date) == str:
        date = to_date(date)

    for index in range(len(booking)):
        if booking[index].booking_date == date and booking[index].time_slot == slot:
            return "Doc"

    contact = Contact.objects.get(user_id=patient_id)
    booking = Booking.objects.filter(contact_id=contact.id)

    if type(date) == str:
        date = to_date(date)

    for index in range(len(booking)):
        if booking[index].booking_date == date and booking[index].time_slot == slot:
            return "Pat"

    return None


def check_bookings(today):

    booking = Booking.objects.all()

    for index in range(len(booking)):
        if booking[index].booking_date < today:
            his = History()
            his.add_to_history(booking[index].id, booking[index].contact.user.username, booking[index].doctor.name, booking[index].contact.user_id, booking[index].doctor_id, booking[index].booking_date,  booking[index].time_slot)
            his.save()
            booking[index].delete()


def age(dob):

    today = datetime.date.today()

    if today.month == dob.month:
        return str(today.day - dob.day)+" Day(s)"
    if today.year == dob.year:
        return str(today.month - dob.month)+" Month(s)"

    return str(today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))+" Year(s)"

# models starts from here


class Doctor(models.Model):

    name = models.CharField(max_length=80)

    age = models.CharField(max_length=4)

    gender = models.CharField(max_length=6, default="other")

    experience = models.CharField(max_length=4)

    domain = models.CharField(max_length=30)

    office_number = models.CharField(max_length=11)

    profile_pic = models.ImageField(
        null=True, default="null", upload_to="doctor_profile")

    """slots = models.CharField(max_length=7, default="")
    
    def set_slot(self, slot):
        
        self.slots=slot
    
    def add_slot(self, slot):
        
        self.slots=self.slots+slot"""

    def __str__(self):
        return str(self.id)+" - "+self.name+" - "+self.gender+" - "+self.domain

    def get_dict(self):
        return {
            "doctor_id": self.id,
            "name": self.name,
            "gender": self.gender,
            "domain": self.domain,
            "ofiice_number": self.office_number
        }


class Contact(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(max_length=10, default="other")

    dob = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    address = models.CharField(max_length=80)

    phone = models.CharField(max_length=11)

    profile_pic = models.ImageField(
        null=True, default="null", upload_to="profile_pics")

    def make_contact(self, user, gender, dob, address, phone):
        self.user = user
        self.gender = gender
        self.dob = dob
        self.address = address
        self.phone = phone

    def __str__(self):
        return str(self.user.id)+" - "+str(self.user.username)+" - "+self.gender+" - "+self.phone+" - "+str(self.dob)

    def get_dict(self):
        return {
            "id": self.user.id,
            "name": self.user.first_name,
            "username": self.user.username,
            "gender": self.gender
        }


class Details(models.Model):

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date_of_visit = models.DateField(
        auto_now_add=False, auto_now=False, blank=True)

    purpose = models.CharField(max_length=30, default="General Check up")

    detail = models.ImageField(null=True)

    def __str__(self):
        return str(self.contact.user.first_name)+" - "+str(self.doctor.name)+" - "+self.purpose+" - "+str(self.date_of_visit)

    def get_dict(self):
        return {
            "entry_id": self.id,
            "user": self.contact.get_dict(),
            "doctor": self.doctor.get_dict(),
            "date_of_visit": self.date_of_visit,
            "purpose": self.purpose
        }


class Reports(models.Model):

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    lab = models.CharField(max_length=40, default="General")

    date_of_report = models.DateField(
        auto_now_add=False, auto_now=False, blank=True)

    report_status = models.BooleanField(default=False)

    report_img = models.ImageField(null=True)

    def __str__(self):
        return str(self.id)+" - "+str(self.contact.user.first_name)+" - "+str(self.doctor.name)+" - "+str(self.report_status)+" - "+str(self.date_of_report)

    def get_dict(self):
        return {
            "id": self.id,
            "contact": self.contact.get_dict(),
            "doctor": self.doctor.get_dict(),
            "lab": self.lab,
            "date_of_report": self.date_of_report,
            "report_genrated": self.report_status,
        }


class Booking(models.Model):

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    booking_date = models.DateField(
        auto_now_add=False, auto_now=False, blank=True)

    time_slot = models.CharField(max_length=10, default="0")

    def make_booking(self, contact, doctor, booking_date, time_slot, patient_name=None, doctor_name=None):
        self.contact = contact
        self.doctor = doctor
        self.booking_date = booking_date
        self.time_slot = time_slot

    def __str__(self):
        return self.contact.user.first_name+" - "+self.doctor.name+" - "+str(self.booking_date)+" - "+self.time_slot

    def get_dict(self):
        return {
            "Booking_id": self.id,
            "patient": self.contact.get_dict(),
            "doctor": self.doctor.get_dict(),
            "booking_date": self.booking_date,
            "time_slot": self.time_slot
        }


class History(models.Model):

    book_no = models.CharField(max_length=200)

    patient_name = models.CharField(max_length=200)

    doctor_name = models.CharField(max_length=200)

    patient_id = models.CharField(max_length=200)

    doctor_id = models.CharField(max_length=200)

    book_date = models.DateField(
        auto_now_add=False, auto_now=False, blank=True)

    book_slot = models.CharField(max_length=100)

    reason = models.CharField(max_length=200, default="--------")

    def add_to_history(self, book_no, patient_name, doctor_name, patient_id, doctor_id, date, slot):
        self.book_no = book_no
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.book_date = date
        self.book_slot = slot

    def __str__(self):
        return str(self.id)+" - "+str(self.book_no)+" - "+str(self.patient_name)+" - "+str(self.doctor_name)+" - "+str(self.book_date)+" - "+str(self.book_slot)
