# Generated by Django 4.2.7 on 2023-11-14 17:56

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_alter_uploadresume_resume_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateResumeOnIndeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_per_hour', models.FloatField()),
                ('experience', models.CharField(choices=[('INT', 'Intern'), ('JNR', 'Junior'), ('MDL', 'Middle'), ('SNR', 'Strong')], max_length=3)),
                ('about', models.TextField()),
                ('programming_languages', models.CharField(choices=[('python', 'Python'), ('java', 'Java'), ('javascript', 'JavaScript'), ('csharp', 'C#'), ('cpp', 'C++'), ('ruby', 'Ruby'), ('php', 'PHP'), ('go', 'Go'), ('html', 'HTML'), ('css', 'CSS'), ('typescript', 'TypeScript'), ('dotnet', '.Net')], max_length=20)),
                ('skills', models.CharField(max_length=20)),
                ('frameworks', models.TextField()),
                ('education', models.TextField()),
                ('certifications', models.FileField(upload_to=accounts.models.slugify_upload)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]