"""
URL configuration for HR_System project.

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
from django.contrib import admin
from django.urls import path, include
from candidates.views import register_candidate, list_candidates_view, download_resume_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/candidates/", include("candidates.urls")),
    path('register/', register_candidate, name='register_candidate'),
    path('candidates/', list_candidates_view, name='list_candidates'),
    path('candidates/<int:pk>/download/', download_resume_view, name='download_resume'),

]
