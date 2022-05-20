from django.urls import path
from api import views as api

app_name = "api"

urlpatterns = [
    # OpenCV
    path("images/opencv", api.OpenCVImageResize.as_view(), name="opencv-image-resize"),
]