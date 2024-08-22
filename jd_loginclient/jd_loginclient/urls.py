
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from main.views import RegisterView, register_confirm, ProfileView
from jd_api.views import GetUrl_Api, test_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
    path("register_confirm/<token>/", register_confirm, name="register_confirm"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("check_email/", TemplateView.as_view(template_name="main/check_email.html"), name="check_email"),

    path("geturl/", GetUrl_Api.as_view()),
    path("test/", test_view)
]
