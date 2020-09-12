"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

# password_reset 기능 구현을 위해 필요한 거 import
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('app/index/', app.views.index, name='index'),
    path('app/create/', app.views.create, name='create'),
    path('app/new/', app.views.blogform, name='new'),
    path('app/<int:pk>/edit/', app.views.edit, name='edit'),
    path('app/<int:pk>/remove/', app.views.remove, name='remove'),
    path('app/<int:blog_id>', app.views.detail, name="detail"),
    path('app/signin/', app.views.signin, name="signin"),
    path('app/', include('django.contrib.auth.urls')),
    path('app/signup/', app.views.signup, name="signup"),
    # password_reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
