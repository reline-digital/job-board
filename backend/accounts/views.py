from rest_framework.decorators import api_view
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


@api_view(['POST'])
def register_user(request):
    user_form = UserRegistrationForm(data=request.data)
    if user_form.is_valid():
        # Create a new user object but avoid saving it yet
        new_user = user_form.save(commit=False)
        # Set the chosen password
        new_user.set_password(user_form.cleaned_data['password1'])
        new_user.save()
        return Response({"message": "User registered successfully."},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    login_form = UserLoginForm(data=request.data)

    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'message': 'Login successful'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is inactive'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid username or password'},
                            status=status.HTTP_401_UNAUTHORIZED)
    return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
def password_reset_confirm(request, uidb64, token):
    form = SetNewPasswordForm(data=request.data, uidb64=uidb64, token=token)

    if form.is_valid():
        form.save()
        return Response({"message": "Password has been reset successfully."},
                        status=status.HTTP_200_OK)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
