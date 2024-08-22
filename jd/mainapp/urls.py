
from django.urls import path
from mainapp.views import main_page

app_name="mainapp"

urlpatterns = [
    path("", main_page, name='main_page')
]