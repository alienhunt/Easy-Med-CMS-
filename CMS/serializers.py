from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Contact,  History, to_date


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email"
        ]


class ContactSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Contact
        fields = "__all__"
        # fields = [
        #     "user",
        #     "gender", 
        #     "dob",
        #     "address",
        #     "phone"
        # ]

    def create(self, validated_data):

        print("ContactSerializer:", validated_data)
        user_data = validated_data.pop("user") 
        
        try:
            
            password = user_data.pop("password")
            
            if "last_name" in user_data.keys():
                lastname = user_data.pop("last_name")
            else:
                lastname = ""

            user = User.objects.create(username=user_data["first_name"]+"_"+user_data["email"], email=user_data.pop("email"), first_name=user_data["first_name"], last_name=lastname)
            user.set_password(password)
            user.save()
            dob = to_date(validated_data.pop("dob"))
            contact = Contact.objects.create(user=user, dob=dob, **validated_data)
            return contact
        
        except Exception as error:
            print("[INTERNAL-ERROR]", error)
            return error


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = "__all__"
