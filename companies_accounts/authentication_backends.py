# companies_accounts/authentication_backends.py
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from .models import CompanyProfile

class CompanyAuthBackend(BaseBackend):
    def authenticate(self, request, patent_number=None, password=None):
        try:
            company_profile = CompanyProfile.objects.get(patent_number=patent_number)
            if check_password(password, company_profile.hash_password):
                return company_profile
        except CompanyProfile.DoesNotExist:
            pass
        return None

    def get_user(self, patent_number):
        try:
            return CompanyProfile.objects.get(patent_number=patent_number)
        except CompanyProfile.DoesNotExist:
            return None



