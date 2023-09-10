from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.models import ModelForm
from .models import Help, Profile, SocialMedia
from cloudinary.forms import CloudinaryFileField      

class ProfileForm(forms.ModelForm):
    """ProfileForm definition."""
    dp = CloudinaryFileField(
        options = {'tags': "influencers_images",})
    full_name = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': "input"}))
    whatsapp = forms.CharField(max_length=20,  widget=forms.TextInput(attrs={'class': "input",'type':"tel"}))
    email = forms.EmailField(max_length=150,  widget=forms.EmailInput(attrs={'class': "input"}))
    birth_date = forms.DateField( widget=forms.DateInput(attrs={'class': "input", 'type':"date"}) )
    class Meta:
        model = Profile
        fields = ('dp','full_name', 'whatsapp', 'email', 'birth_date')


class JobFeedbackForm(forms.Form):
    screenshot = CloudinaryFileField(options = {'tags': "screenshots",})
    views = forms.IntegerField( widget = forms.NumberInput(attrs={'class':"input"}))

class HelpForm(forms.ModelForm):
    """HelpForm definition."""
    description  = forms.CharField(max_length=500, widget=forms.Textarea())
    class Meta:
        model = Help
        fields = ('description',)
class AccountApprovalForm(forms.Form):
    ig_username =  forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': "input"}))
    screenshot = CloudinaryFileField(options = {'tags': "verification_screenshots",})
    views = forms.IntegerField(max_value=10000)
