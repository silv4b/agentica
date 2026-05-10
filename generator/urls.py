from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name="result"),
    path("download/", views.download, name="download"),
    path("download-raw/", views.download_raw, name="download_raw"),
    path("create-gist/", views.create_gist, name="create_gist"),
]
