from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from .views import PasswordsChangeView, Details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='music_site/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='music_site/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password/', PasswordsChangeView.as_view(template_name='music_site/change-password.html'), name='password'),
    path('upload/', views.upload, name='upload'),
    path('upload_list/', views.upload_list, name='upload_list'),
    path('upload/<int:pk>/', views.delete, name='delete'),
    path('upload_detail/<int:pk>/', Details.as_view(), name='details'),
    path('add_sample/<int:pk1>/<int:pk2>/', views.addSample, name='add_sample'),
    path('detail/<int:pk>/<int:pk1>/<int:pk2>/', views.deleteSample, name='delete_sample'),
    path('', TemplateView.as_view(template_name='music_site/welcome.html'), name='welcome'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
