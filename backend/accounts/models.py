from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    employer = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
