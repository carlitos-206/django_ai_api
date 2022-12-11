from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index),
    path("ai_img_creator", views.imgAiCreation)
]