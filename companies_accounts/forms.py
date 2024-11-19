from django import forms
from .models import CompanyProfile, OwnerTable

class CompanyRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_slogan']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class OwnerTableForm(forms.ModelForm):
    class Meta:
        model = OwnerTable
        fields = '__all__'

class CompanyLoginForm(forms.ModelForm):

    patent_number = forms.CharField()
 
    class Meta:
        model = CompanyProfile
        fields = ('patent_number','hash_password')
    
    def verify_tel(self):
        patent_number = self.cleaned_data.get("patent_number")
        if patent_number and len(patent_number) != 10:
            raise forms.ValidationError("The Phone Number is not correct")