from django_filters import rest_framework as filters

from .models import CreateResumeOnIndeed, UploadJob


class ResumeFilter(filters.FilterSet):
    class Meta:
        model = CreateResumeOnIndeed
        fields = ('salary_per_hour', 'experience', 'programming_languages', 'skills', 'frameworks',)


class JobFilter(filters.FilterSet):
    class Meta:
        model = UploadJob
        fields = {
            'company_name': ['exact', 'icontains'],
            'job_title': ['exact', 'icontains'],
            'state': ['exact'],
            'number_of_employers': ['exact'],
            'work_location': ['exact'],
            'job_type': ['exact'],
            'job_schedule': ['exact'],
            'experience_level_for_job': ['exact', 'icontains'],
            'salary_min': ['exact', 'gte', 'lte'],
            'salary_max': ['exact', 'gte', 'lte'],
            'compensation_package': ['exact'],
            'resume_choice': ['exact'],
            'skills': ['exact'],
            'person': ['exact'],
            'industry': ['exact'],
        }
