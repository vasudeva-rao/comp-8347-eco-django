from django.contrib import admin
from django.urls import path
from myapp.views import log_eco_action, ecoaction_success, profile, rewards, home, leaderboard, register, about, contact, team, admin_console
from myapp.forms import CustomPasswordResetForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('log-action/', log_eco_action, name='log_eco_action'),
    path('log-action/success/', ecoaction_success, name='ecoaction_success'),
    path('profile/', profile, name='profile'),
    path('rewards/', rewards, name='rewards'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('team/', team, name='team'),
    path('admin-console/', admin_console, name='admin_console'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
