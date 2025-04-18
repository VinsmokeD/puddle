from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)  # This automatically clears the session
    return redirect('core:login')
