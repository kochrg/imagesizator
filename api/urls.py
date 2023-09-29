from django.urls import path
from api import views as api

app_name = "api"

# GENERIC
urlpatterns = [
    # Scheduler
    path(
        "scheduler/delete_expired_files",
        api.DeleteExpiredFilesView.as_view(),
        name="delete-expired-files",
    ),
]

# API V-1.1
# action    = publish   | retrieve
# service   = pillow    | opencv
# protected = protected | public
# static    = static    | temp
# folder    = static    | temp

urlpatterns += [
    # Work with an image service and publish/retrieve the result
    path(
        "<action>/image/<service>/<protected>/<static>",
        api.PublishRetrieveImageResizeView.as_view(),
        name="new-image-resize-publish-retrieve",
    ),
    # Publish any type of file without modifications
    path(
        "publish/<protected>/<static>",
        api.NewPublishFile.as_view(),
        name="new-publish-file",
    ),
]
