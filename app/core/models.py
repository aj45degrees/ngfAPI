# import uuid
# import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a pdf"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name



class PDFData(models.Model):
    business_legal_name = models.CharField(max_length=125) # required
    dba_or_tradename = models.CharField(blank=True, max_length=100)
    business_address_row1 = models.CharField(blank=True, max_length=80) # required
    business_address_row2 = models.CharField(blank=True, max_length=80) # required
    # this is a 6 digit number that on their application 
    naics_code = models.PositiveIntegerField(default=0) # required
    # must match the loan forgiveness application
    business_tin_ein_ssn = models.PositiveIntegerField(default=0) # required
    business_phone = models.PositiveIntegerField(default=0) # required
    primary_contact = models.CharField(max_length=80) # required
    email = models.EmailField(max_length=255) # required
    # if one is selected then gray out the other
    first_draw_checkbox = models.BooleanField(default=False) # required
    second_draw_checkbox = models.BooleanField(default=False) # or required
    # this is a 10 digit number
    sba_loan_number = models.PositiveIntegerField(default=0) # required
    lender_loan_number = models.CharField(blank=True, max_length=255) # required
    ppp_loan_amount = models.PositiveIntegerField(default=0) # required
    ppp_loan_disbursement_date = models.DateField(null=True, blank=True) # required
    ppp_loan_increase = models.PositiveIntegerField(default=0)
    ppp_loan_increase_date = models.DateField(null=True, blank=True)
    employees_at_application = models.PositiveIntegerField(default=0) # required
    employees_at_forgiveness = models.PositiveIntegerField(default=0) # required
    # this should equal the loan disbursement date
    covered_period_beg = models.DateField(null=True, blank=True) # required
    # >= 8 weeks <= 24 weeks from the beginning date
    covered_period_end = models.DateField(null=True, blank=True) # required
    # >= 60% of the loan amount
    loan_spent_on_payroll = models.PositiveIntegerField(default=0) # required
    # <= total loan amount
    requested_forgiveness_amount = models.PositiveIntegerField(default=0) # required
    signature_date = models.DateField(null=True, blank=True)
    print_name = models.CharField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=100)
    complete_volutary_disclosure = models.BooleanField(default=False)
    principal_name = models.CharField(blank=True, max_length=255)
    principal_position = models.CharField(blank=True, max_length=255)
    veteran_non_veteran = models.BooleanField(default=False)
    veteran_veteran = models.BooleanField(default=False)
    veteran_disabled_veteran = models.BooleanField(default=False)
    veteran_spouse = models.BooleanField(default=False)
    veteran_not_disclosed = models.BooleanField(default=False)
    gender_male = models.BooleanField(default=False)
    gender_female = models.BooleanField(default=False)
    gender_not_disclosed = models.BooleanField(default=False)
    race_native_american = models.BooleanField(default=False)
    race_asian = models.BooleanField(default=False)
    race_black = models.BooleanField(default=False)
    race_pacific_islander = models.BooleanField(default=False)
    race_white = models.BooleanField(default=False)
    race_not_disclosed = models.BooleanField(default=False)
    ethicity_hispanic = models.BooleanField(default=False)
    ethicity_not_hispanic = models.BooleanField(default=False)
    ethicity_not_disclosed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    file_path = models.CharField(max_length=255) # work on tomorrow

    def _str_(self):
        return self.business_legal_name