from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Doctor)

admin.site.register(Contact)

admin.site.register(Booking)

admin.site.register(Details)

admin.site.register(History)

admin.site.register(Reports)


# changing the admin site header

admin.site.site_header = "CMS Admin"

admin.site.site_title = "CMS Administrator"

admin.site.index_title = "Clinic Management System Administrator"


# removing the default group model from the admin site

admin.site.unregister(Group)
