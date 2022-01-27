from django import forms
from .models import Contact

class updateContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        labels = {'profile_pic':''} 
        exclude = ['user',]