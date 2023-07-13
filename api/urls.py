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
    # Images
    path(
        "images/<service>",
        api.ImageResizeView.as_view(),
        name="image-resize"
    ),
    # PDF
    path(
        "images/pdf/publish",
        api.PublishPDFFile.as_view(),
        name="publish-pdf-file"
    ),
    # Publish any type of file without modifications
    path(
        "files/publish",
        api.PublishFile.as_view(),
        name="publish-any-file"
    ),
    path(
        "images/viewer/",
        api.browserFileViewer.as_view(),
        name="publish-file-in-browser-viewer"
    ),
]
