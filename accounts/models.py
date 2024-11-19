from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class GamblerProfile(models.Model):
    phone_number_regex = r'^\d{8}$'
    phone_number_validator = RegexValidator(
        regex=phone_number_regex,
        message='Phone number must be exactly 8 digits long.',
        code='invalid_phone_number'
    )
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    profile_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=8,
        validators=[phone_number_validator],
        unique=True
    )
    sex = models.CharField(max_length=255, choices=SEX_CHOICES, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
    
    def validate_past_date(value):
        if value > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")

    def validate_reasonable_date(value):
        # Change the range as needed based on your application's requirements
        min_birth_date = timezone.now().date() - timezone.timedelta(days=365 * 100)  # 100 years ago
        if value < min_birth_date:
            raise ValidationError("Date of birth is too far in the past.")

    date_of_birth = models.DateField(
        validators=[validate_past_date, validate_reasonable_date],
        default=timezone.now,
        null=True
    )

class PasswordChange(models.Model):
    change_password_id = models.AutoField(primary_key=True)
    gambler = models.ForeignKey(GamblerProfile, on_delete=models.CASCADE, to_field='profile_id')
    phone_number_for_new_password = models.CharField(max_length=255,editable=False)
    code_generated_for_new_password = models.CharField(max_length=255)
    hash_new_password = models.CharField(max_length=500)
    changed_password_date = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(default=timezone.now)


class GamblerUserManager(BaseUserManager):
    
    def _create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Set the password hash
        user.save(using=self._db)
        return user
    
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")

        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(phone_number, password, **extra_fields)


class GamblerUser(AbstractBaseUser, PermissionsMixin):
    # Fields from the logical model (except hash_password)
    phone_number_regex = r'^\d{8}$'
    phone_number_validator = RegexValidator(
        regex=phone_number_regex,
        message='Phone number must be exactly 8 digits long.',
        code='invalid_phone_number'
    )
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=8,
        validators=[phone_number_validator],
        unique=True
    )
    sex = models.CharField(max_length=255, choices=SEX_CHOICES, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # Additional fields for custom user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Link to GamblerProfile using a one-to-one relationship
    profile = models.OneToOneField(GamblerProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='user')

    objects = GamblerUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'sex', 'date_of_birth']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def validate_past_date(value):
        if value > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")

    def validate_reasonable_date(value):
        # Change the range as needed based on your application's requirements
        min_birth_date = timezone.now().date() - timezone.timedelta(days=365 * 100)  # 100 years ago
        if value < min_birth_date:
            raise ValidationError("Date of birth is too far in the past.")

    date_of_birth = models.DateField(
        validators=[validate_past_date, validate_reasonable_date],
        default=timezone.now,
        null=True
    )

