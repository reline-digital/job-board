from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Application
from .serializers import ApplicationSerializer
from accounts.models import Job


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'},
                        status=status.HTTP_404_NOT_FOUND)

    application, created = Application.objects.get_or_create(
        job=job, applicant=request.user)
    if not created:
        return Response({'error': 'Application already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_applications(request):
    applications = Application.objects.filter(applicant=request.user)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request, application_id):
    try:
        application = Application.objects.get(id=application_id,
                                              job__employer=request.user)
    except Application.DoesNotExist:
        return Response({'error': 'Application not found or unauthorized'},
                        status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if not new_status:
        return Response({'error': 'Status is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    if new_status not in dict(Application.STATUS_CHOICES):
        return Response({'error': 'Invalid status'},
                        status=status.HTTP_400_BAD_REQUEST)

    application.status = new_status
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_200_OK)
