
from django.urls import path
from mainapp.views import main_page

urlpatterns = [
    path("", main_page)
]