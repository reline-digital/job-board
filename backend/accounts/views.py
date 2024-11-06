from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import JobSerializer
from .models import Job
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
from .forms import *

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from job_board_be import settings
from rest_framework_simplejwt.tokens import RefreshToken


# Function to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    user_form = UserRegistrationForm(data=request.data)
    if user_form.is_valid():
        # Create a new user object but avoid saving it yet
        new_user = user_form.save(commit=False)
        # Set the chosen password
        new_user.set_password(user_form.cleaned_data['password1'])
        new_user.save()

        # Generate JWT tokens for the new user
        tokens = get_tokens_for_user(new_user)

        return Response(
            {
                "message": "User registered successfully.",
                "token": tokens
            },
            status=status.HTTP_201_CREATED)
    else:
        return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    login_form = UserLoginForm(data=request.data)

    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Generate JWT tokens for the user
                tokens = get_tokens_for_user(user)

                return Response(
                    {
                        "message": "Login successful",
                        "tokens": tokens
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is inactive'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid username or password'},
                            status=status.HTTP_401_UNAUTHORIZED)
    return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    form = PasswordResetForm(data=request.data)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = request.build_absolute_uri(
            reverse('password_reset_confirm',
                    kwargs={
                        'uidb64': uid,
                        'token': token
                    }))

        subject = 'Password Reset Request'
        message = (
            f'Hello {user.username}, \n\n'
            'You requested a password reset. Click the link below to reset your password:\n'
            f'{reset_link}\n\n'
            'Thank you!\n\n'
            'If you did not request this change, please ignore this email.')

        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER, [email],
                  fail_silently=False)
        return Response({"message": "Password reset email sent."},
                        status=status.HTTP_200_OK)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    form = SetNewPasswordForm(data=request.data, uidb64=uidb64, token=token)

    if form.is_valid():
        form.save()
        return Response({"message": "Password has been reset successfully."},
                        status=status.HTTP_200_OK)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(employer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(job)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if job.employer != request.user:
        return Response({'error': "You are not authorized to edit this job"},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = JobSerializer(job, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if job.employer != request.user:
        return Response({'error': "You are not authorized to delete this job"},
                        status=status.HTTP_403_FORBIDDEN)

    job.delete()
    return Response({"message": "Job deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT)
