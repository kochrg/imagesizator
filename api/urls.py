from django.urls import path
from api import views as api

app_name = "api"

urlpatterns = [
    # Scheduler
    path(
        "scheduler/delete_expired_files",
        api.DeleteExpiredFilesView.as_view(),
        name="delete-expired-files"
    ),
    # OpenCV
    path(
        "images/opencv",
        api.OpenCVImageResize.as_view(),
        name="opencv-image-resize"
    ),
    # Pillow
    path(
        "images/pillow",
        api.PILImageResize.as_view(),
        name="pillow-image-resize"
    ),
    # PDF
    path(
        "images/pdf/publish",
        api.PublishPDFFile.as_view(),
        name="publish-pdf-file"
    ),
]
