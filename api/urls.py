from django.urls import path
from api import views as api

app_name = "api"

# GENERIC
urlpatterns = [
    # Scheduler
    path(
        "scheduler/delete_expired_files",
        api.DeleteExpiredFilesView.as_view(),
        name="delete-expired-files"
    ),
]

# API V-1.0
urlpatterns += [
    # PDF
    path(
        "images/pdf/publish",
        api.PublishPDFFile.as_view(),
        name="publish-pdf-file"
    ),
    # Images
    path(
        "images/viewer/",
        api.browserFileViewer.as_view(),
        name="publish-file-in-browser-viewer"
    ),
    path(
        "images/<service>",
        api.ImageResizeView.as_view(),
        name="image-resize"
    ),
    # Publish any type of file without modifications
    path(
        "files/publish",
        api.PublishFile.as_view(),
        name="publish-any-file"
    ),
]

# API V-1.1
urlpatterns += [
    # Publish any type of file without modifications
    path(
        "publish/<protected>/<static>",
        api.NewPublishFile.as_view(),
        name="new-publish-file"
    ),
]