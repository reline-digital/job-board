from django.urls import path
from .views import (
    register_user, login_user, password_reset,
    password_reset_confirm, list_jobs, create_job, retrieve_job, update_job, delete_job
)

urlpatterns = [
    # Authentication
    path('api/signup/', register_user, name="register"),
    path('api/login/', login_user, name="login"),
    path('password-reset/', password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),

    # Jobs
    path('jobs/', list_jobs, name='list-jobs'),
    path('jobs/create/', create_job, name='create-job'),
    path('jobs/<int:pk>/', retrieve_job, name='retrieve-job'),
    path('jobs/<int:pk>/update/', update_job, name='update-job'),
    path('jobs/<int:pk>/delete/', delete_job, name='delete-job'),
]
