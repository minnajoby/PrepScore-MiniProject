"""
URL configuration for prepscore_project project.

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
# In prepscore_project/urls.py

from django.contrib import admin
from django.urls import path, include

# --- REMOVED the import for CustomSetPasswordForm ---
from django.contrib.auth import views as auth_views
# --- We don't need the custom view anymore either ---

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # We can now rely on the default view, which will find our beautiful template
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('profiles.urls')),
]