from django.db import models
from django.contrib.auth.models import User
from accounts.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('seen', 'Seen'),
        ('considered', 'Considered'),
        ('declined', 'Declined'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title} ({self.status})"
