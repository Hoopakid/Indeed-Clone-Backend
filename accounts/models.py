from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserContactInformation(models.Model):
    class EmployerOrSeeker(models.IntegerChoices):
        EMPLOYER = 1, _('Employer')
        SEEKER = 2, _('Seeker')

    class EmploymentEligibilityChoices(models.IntegerChoices):
        AUTHORIZED = 1, _("Authorized to work in the US for any employer")
        SPONSORSHIP = 2, _("Sponsorship required to work in the US")
        NOT_SPECIFIED = 0, _("Not specified")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    headline = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    employment_eligibility = models.IntegerField(choices=EmploymentEligibilityChoices.choices, max_length=1)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    whoami = models.IntegerField(choices=EmployerOrSeeker.choices, blank=True, null=True)

    def __str__(self):
        return self.first_name + self.last_name
