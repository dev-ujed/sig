from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = getattr(settings, 'LOGIN_EXEMPT_URLS', [])

    def __call__(self, request):
        current_url = resolve(request.path_info).url_name

        if not request.user.is_authenticated:
            if not any(request.path_info.startswith(url) for url in self.exempt_urls):
                return redirect('/') 

        return self.get_response(request)
