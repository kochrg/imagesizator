"""imagesizator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from api import views as api

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    # Accessing files
    path(
        "www/public/<folder>/<file_name>",
        api.PublicBrowserFileViewer.as_view(),
        name="public-browser-file-viewer",
    ),
    path(
        "www/protected/<folder>/<file_name>",
        api.UnsecureProtectedBrowserFileViewer.as_view(),
        name="protected-browser-file-viewer",
    ),
    path(
        "www/protected/<folder>/<file_name>/<token>",
        api.ProtectedBrowserFileViewer.as_view(),
        name="protected-browser-file-viewer",
    ),
]
