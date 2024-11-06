from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'status', 'applied_at']
        read_only_fields = ['job', 'applicant', 'applied_at']
