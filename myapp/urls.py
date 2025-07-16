from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('tips/', views.TipListView.as_view(), name='tips-list'),
    path('tip/<int:pk>/', views.TipDetailView.as_view(), name='tip-detail'),
    path('tip/<int:pk>/edit/', views.TipUpdateView.as_view(), name='tip-edit'),
    path('tip/<int:pk>/delete/', views.TipDeleteView.as_view(), name='tip-delete'),
    path('tip/add/', views.TipCreateView.as_view(), name='tip-add'),
    path('upload/', views.UserUploadCreateView.as_view(), name='upload'),
    path('uploads/', views.UploadGalleryView.as_view(), name='upload-gallery'),
    path('bookmark/<int:pk>/', views.bookmark_tip, name='bookmark-tip'),
    path('unbookmark/<int:pk>/', views.unbookmark_tip, name='unbookmark-tip'),
    path('history/', views.VisitHistoryView.as_view(), name='visit-history'),
] 