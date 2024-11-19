from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils import timezone

class OwnerTable(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_first_name = models.CharField(max_length=255)
    owner_last_name = models.CharField(max_length=255)
    owner_phone_1 = models.CharField(max_length=255)
    owner_phone_2 = models.CharField(max_length=255, blank=True, null=True)
    owner_email = models.EmailField(max_length=255)
    owner_department = models.CharField(max_length=255)
    owner_city = models.CharField(max_length=255)
    owner_address = models.CharField(max_length=255)
    owner_profession = models.CharField(max_length=255)
    owner_NIF = models.CharField(max_length=255)
    owner_cin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.owner_first_name} {self.owner_last_name}"

class CompanyProfile(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    patent_number = models.CharField(max_length=255, unique=True, default='none')
    company_slogan = models.CharField(max_length=255)
    owner = models.OneToOneField(OwnerTable, on_delete=models.CASCADE)
    company_type = models.CharField(max_length=255)
    hash_password = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.hash_password)
