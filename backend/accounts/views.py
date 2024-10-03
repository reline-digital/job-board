from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
from .forms import *

@api_view(['POST'])
def register_user(request):
    user_form = UserRegistrationForm(data=request.data)
    if user_form.is_valid():
        # Create a new user object but avoid saving it yet
        new_user = user_form.save(commit=False)
        # Set the chosen password
        new_user.set_password(user_form.cleaned_data['password1'])
        new_user.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
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
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is inactive'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)
