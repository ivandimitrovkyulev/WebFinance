from typing import Any
from django.views.generic import TemplateView
from allauth.account.utils import has_verified_email


class HomeView(TemplateView):
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs) -> dict[Any, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["user_email_is_verified"] = has_verified_email(self.request.user)

        return context
