# adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.name = sociallogin.account.extra_data.get('given_name', '')
        user.last_name = sociallogin.account.extra_data.get('family_name', '')
        user.save()
        return user