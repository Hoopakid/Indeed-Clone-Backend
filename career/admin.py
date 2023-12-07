from django.contrib import admin

from career.models import Industry, SalaryByIndustry, Chat, Message

admin.site.register((Industry, SalaryByIndustry, Chat, Message))
