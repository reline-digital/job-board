from django.urls import path
from .views import apply_for_job, view_applications, update_application_status

urlpatterns = [
    path('apply/<int:job_id>/', apply_for_job, name='apply-for-job'),
    path('applications/', view_applications, name='view-applications'),
    path('applications/<int:application_id>/update/', update_application_status, name='update-application-status'),
]
