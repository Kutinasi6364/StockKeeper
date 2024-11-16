from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy

class LoginView(auth_view.LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')


class LogoutView(auth_view.LogoutView):
    next_page = reverse_lazy('login')