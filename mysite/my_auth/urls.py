from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile_view, logout_view

app_name = 'my_auth'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='my_auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='my_auth/logout.html'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
