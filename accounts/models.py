from os.path import splitext

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


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

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
    certifications = models.FileField(upload_to=slugify_upload)
    created_date = models.DateTimeField(auto_now_add=True)


class UploadResume(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    resume = models.FileField(upload_to=slugify_upload)
