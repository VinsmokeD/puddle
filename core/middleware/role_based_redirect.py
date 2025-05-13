from django.urls import reverse
from django.shortcuts import redirect

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Allow unauthenticated users to access login/signup
        allowed_paths = [
            reverse('core:login'),
            reverse('core:signup'),
            reverse('core:index'),  # you can adjust
        ]

        if not request.user.is_authenticated:
            if path not in allowed_paths:
                return redirect('core:login')

        # If user is authenticated
        if request.user.is_authenticated:
            if hasattr(request.user, 'role'):  # assuming you have a 'role' field
                if request.user.role == 'customer':
                    browse_path = reverse('core:browse')
                    if path != browse_path:
                        return redirect('core:browse')

        response = self.get_response(request)
        return response
