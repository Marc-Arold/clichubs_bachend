# accounts/forms.py

from django import forms
from .models import GamblerUser

class GamblerUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = GamblerUser
        fields = ('phone_number', 'first_name', 'last_name', 'sex', 'date_of_birth','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def verify_tel(self):
        telephone = self.cleaned_data.get("phone_number")
        if telephone and len(telephone) != 8:
            raise forms.ValidationError("The Phone Number is not correct")

    def save(self, commit=True):
        user = super(GamblerUserCreationForm).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class GamblerLoginForm(forms.ModelForm):

    telephone = forms.CharField()
 
    class Meta:
        model = GamblerUser
        fields = ('phone_number','password')
    
    def verify_tel(self):
        telephone = self.cleaned_data.get("phone_number")
        if telephone and len(telephone) != 8:
            raise forms.ValidationError("The Phone Number is not correct")
        
