from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserContactInformation(models.Model):
    class EmploymentEligibilityChoices(models.IntegerChoices):
        AUTHORIZED = 1, "Authorized to work in the US for any employer"
        SPONSORSHIP = 2, "Sponsorship required to work in the US"
        NOT_SPECIFIED = 0, "Not specified"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    headline = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    employment_eligibility = models.CharField(choices=EmploymentEligibilityChoices.choices, max_length=1)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + self.last_name
