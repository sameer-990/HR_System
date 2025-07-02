from django.db import models
from django.core.validators import FileExtensionValidator
from .storage import get_resume_storage


def resume_upload_path(instance, filename):
    # Store by candidate ID and upload date
    # Store files in a structured manner (e.g., by user ID).
    return f"resumes/{instance.id}/{filename}"


class Candidate(models.Model):
    DEPARTMENTS = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Finance', 'Finance'),
    ]

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted')
    ]

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    experience_years = models.PositiveIntegerField()
    department = models.CharField(choices=DEPARTMENTS, max_length=20)
    email = models.EmailField(unique=True)
    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx'])
        ],
        storage=get_resume_storage()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Submitted')

    class Meta:
        indexes = [
            models.Index(fields=["department", "created_at"], name="dept_regdate_idx"),
        ]

    def __str__(self):
        return self.full_name


class ApplicationStatus(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(choices=Candidate.STATUS_CHOICES, max_length=30)
    feedback = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)  # Admin name from header

    class Meta:
        ordering = ['-updated_at']
