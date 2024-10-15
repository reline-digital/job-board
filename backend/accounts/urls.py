from django.urls import path
from .views import register_user, login_user, password_reset, password_reset_confirm

urlpatterns = [
    path('api/signup/', register_user, name="register"),
    path('api/login/', login_user, name="login"),
    path('password-reset/', password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
