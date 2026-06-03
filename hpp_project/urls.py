"""
URL configuration for hpp_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('prediction/', views.prediction, name='prediction'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('user_login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('user_dashboard/', views.dashboard, name='dashboard'),
    path('logout/',views.user_logout, name='logout'),
    path('update-photo/', views.update_photo, name='update_photo'),
    path('admin-panel/',views.admin_panel, name='admin_panel'),
    path('admin-panel/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-panel/predictions/', views.admin_all_predictions, name='admin_all_predictions'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
