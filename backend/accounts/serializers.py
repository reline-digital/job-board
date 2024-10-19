from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'requirements', 'salary',
            'location', 'created_at'
        ]
        read_only_fields = ['employer', 'created_at']
