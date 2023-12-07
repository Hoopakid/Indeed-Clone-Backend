from os.path import splitext

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from accounts.models import UserContactInformation
from career.models import Industry


class Discount(models.Model):
    percentage_of_discount = models.IntegerField()


class PaymentOption(models.Model):
    month_trial = models.IntegerField()
    price = models.FloatField()
    option_description = models.TextField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __int__(self):
        return self.month_trial


class PaymentStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "PaymentStatus"
        verbose_name_plural = "PaymentStatus"


class UserPaymentCard(models.Model):
    card_number = models.IntegerField()
    expiry_date = models.CharField(max_length=5)
    security_code = models.IntegerField()
    name_of_card = models.CharField(max_length=50)
    address = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE,
                                related_name='userpaymentcard_address')
    country = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE,
                                related_name='userpaymentcard_country')
    city = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE, related_name='userpaymentcard_city')
    postal_code = models.ForeignKey(UserContactInformation, on_delete=models.CASCADE,
                                    related_name='userpaymentcard_postal_code')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    payment_default_balance = models.FloatField(blank=True, null=True, default=10000)

    def __str__(self):
        return self.user.first_name


class UserPaymentModel(models.Model):
    option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    payed_amount = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option.month_trial


class JobCreate(models.Model):
    YES = 1
    NO = 0

    STATUS_CHOICES = (
        (YES, 'This user can create jobs for our website'),
        (NO, "This user can't create jobs for our website")
    )

    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class JobType(models.Model):
    job_type = models.CharField(max_length=255)

    def __str__(self):
        return self.job_type


class JobSchedule(models.Model):
    job_schedule = models.CharField(max_length=255)

    def __str__(self):
        return self.job_schedule


class CompensationPackage(models.Model):
    job_package = models.CharField(max_length=255)

    def __str__(self):
        return self.job_package


class SkillsForJob(models.Model):
    job_skills = models.CharField(max_length=255)

    def __str__(self):
        return self.job_skills


class StateJob(models.Model):
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.state


class UploadJob(models.Model):
    class LocationWorkChoices(models.TextChoices):
        GENERAL = "GNL", _("General Location")
        REMOTE = "RMT", _("Remote")
        HYBRID = "HRD", _("Hybrid Remote")
        PRECISE = "PCS", _("Precise Location")

    class RateWorkChoices(models.TextChoices):
        PER_HOUR = "PH", _("Per hour")
        PER_DAY = "PD", _("Per day")
        PER_WEEK = "PW", _("Per week")
        PER_MONTH = "PM", _("Per month")
        PER_YEAR = "PY", _("Per year")

    HEARDCHOICES = [
        ('social media', 'Social Media'),
        ('mail', 'Mail'),
        ('search engine', 'Search Engine (Google, Bing, Yahoo)'),
        ('online video', 'Online Video'),
        ('newspaper', 'Newspaper'),
        ('radio', 'Radio'),
        ('other', 'Other'),
    ]

    class ResumeIntegerChoice(models.TextChoices):
        RESUME_NEED = "1", _('Yes, require a resume')
        IF_WANTS = "2", _('Give the option to include a resume')
        NO_NEED_RESUME = "3", _("No, don't ask for a resume")

    class PersonChoice(models.TextChoices):
        MALE = "1", _('Male'),
        FEMALE = "2", _('Female'),
        UNIDENTIFIED = "0", _('Unidentified'),

    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    heard_about_us = models.CharField(choices=HEARDCHOICES, max_length=155)
    job_title = models.CharField(max_length=255)
    state = models.ForeignKey(StateJob, on_delete=models.CASCADE)
    number_of_employers = models.IntegerField(default=1)
    work_location = models.CharField(choices=LocationWorkChoices.choices, max_length=255)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    job_schedule = models.ForeignKey(JobSchedule, on_delete=models.CASCADE)
    experience_level_for_job = models.CharField(max_length=255)
    salary_min = models.FloatField(default=0, blank=True)
    salary_max = models.FloatField(default=100, blank=True)
    rate_salary = models.CharField(max_length=255, choices=RateWorkChoices.choices)
    compensation_package = models.ForeignKey(CompensationPackage, on_delete=models.CASCADE)
    job_description = models.TextField()
    resume_choice = models.CharField(max_length=255, choices=ResumeIntegerChoice.choices)
    skills = models.ForeignKey(SkillsForJob, on_delete=models.CASCADE)
    benefits = models.CharField(max_length=255, blank=True, null=True)
    job_website = models.URLField(max_length=200, blank=True, null=True)
    person = models.CharField(choices=PersonChoice.choices, blank=True, null=True)
    industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title


class ApplyJob(models.Model):
    job = models.ForeignKey(UploadJob, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.job_title


def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class CreateResumeOnIndeed(models.Model):
    class Experience(models.TextChoices):
        INTERN = "INT", _("Intern")
        JUNIOR = "JNR", _("Junior")
        MIDDLE = "MDL", _("Middle")
        SENIOR = "SNR", _("Strong")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary_per_hour = models.FloatField()
    experience = models.CharField(choices=Experience.choices, max_length=3)
    about = models.TextField()
    PROGRAMMING_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('php', 'PHP'),
        ('go', 'Go'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('typescript', 'TypeScript'),
        ('dotnet', '.Net'),
    ]
    programming_languages = models.CharField(choices=PROGRAMMING_CHOICES, max_length=20)
    skills = models.CharField(max_length=20)
    frameworks = models.TextField()
    education = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name


class UploadResumeWithFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to=slugify_upload)

    def __str__(self):
        return self.user.first_name + self.user.last_name
