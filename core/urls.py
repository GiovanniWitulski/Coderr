"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# Django Imports
from django.contrib import admin
from django.urls import path, include

# Local Imports
from core.views import BaseInfoView

urlpatterns = [
    # 1. Django Admin Interface
    path('admin/', admin.site.urls),
    
    # 2. Global API Endpoints
    path('api/base-info/', BaseInfoView.as_view(), name='base-info'),
    
    # 3. App-Specific API Endpoints
    # All app URLs are included under the /api/ prefix.
    path('api/', include('offers_app.api.urls')),
    path('api/', include('orders_app.api.urls')),
    path('api/', include('reviews_app.api.urls')),
    path('api/', include('user_profile_app.api.urls')),
]
