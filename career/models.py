from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Industry(models.Model):
    industry = models.CharField(max_length=50)

    def __str__(self):
        return self.industry


class SalaryByIndustry(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    openings = models.CharField(max_length=50)
    skills = models.CharField(max_length=50)
    price_per_year = models.FloatField()

    def save(
            self, *args, **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
