from django.urls import path
from .views import create_resume, preview

urlpatterns = [
    # Single page: manual + upload + autofill
    path("", create_resume, name="create"),

    # Preview & download
    path("preview/<int:resume_id>/", preview, name="preview"),
]
