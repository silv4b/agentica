from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name="result"),
    path("download/", views.download, name="download"),
    path("create-gist/", views.create_gist, name="create_gist"),
]
