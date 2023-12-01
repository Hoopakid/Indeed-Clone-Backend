from django.db import models
from django.template.defaultfilters import slugify


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
