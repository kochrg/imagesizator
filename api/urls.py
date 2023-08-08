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
    # Images
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
    # Work with an image service and publish/retrieve the result
    path(
        "<action>/image/<service>/<protected>/<static>",
        api.PublishRetrieveImageResizeView.as_view(),
        name="new-image-resize-publish-retrieve"
    ),
    # Publish any type of file without modifications
    path(
        "publish/<protected>/<static>",
        api.NewPublishFile.as_view(),
        name="new-publish-file"
    ),
    # Accessing files
    path(
        "www/public/<folder>/<file_name>",
        api.PublicBrowserFileViewer.as_view(),
        name="public-browser-file-viewer"
    )
]