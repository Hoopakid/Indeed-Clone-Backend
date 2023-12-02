from django.contrib import admin

from .models import *

admin.site.register((Discount, ApplyJob, PaymentOption, PaymentStatus, UserPaymentModel, UserPaymentCard, JobCreate,
                     JobType, JobSchedule, StateJob, CreateResumeOnIndeed, CompensationPackage, UploadJob,
                     UploadResumeWithFile, SkillsForJob))
