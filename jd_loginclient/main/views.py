from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView, ListView
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from main.models import CustomUser
from django.utils.translation import gettext_lazy as _


from uuid import uuid4
from django.conf import settings
from django.core.cache import cache


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "main/register.html"
    success_url = reverse_lazy("check_email")

    def form_valid(self, form):
        custom_user, created = CustomUser.objects.get_or_create(email=form.cleaned_data["email"])


        if created:
            custom_user.set_password(form.cleaned_data["password"])
            custom_user.save(update_fields=["password", ])


        if custom_user.is_active is False:
            token = uuid4().hex
            redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, {"custom_user_id": custom_user.id}, timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT)

            confirm_link = self.request.build_absolute_uri(
                reverse_lazy(
                    "register_confirm", kwargs={"token": token}
                )
            )

            message = _(f'follow this link %s \n' f"to confirm! \n" % confirm_link)

            send_mail(
                subject=_("Please confirm your registration!"),
                message=message,
                from_email="Eltrox822@yandex.ru",
                recipient_list=[custom_user.email, ]
            )

        return super().form_valid(form)
        

def register_confirm(request, token):
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    custom_user_info = cache.get(redis_key) or {}

    if custom_user_id := custom_user_info.get("custom_user_id"):
        custom_user = get_object_or_404(CustomUser, id=custom_user_id)
        custom_user.is_active = True
        custom_user.save(update_fields=["is_active"])
        return redirect(to=reverse_lazy("profile"))

    else:
        return redirect(to=reverse_lazy("register"))
    

class ProfileView(ListView):
    template_name = "main/profile.html"
    model = CustomUser
    context_object_name = "user_info"

    def get_queryset(self):
        return [self.request.user]
    



