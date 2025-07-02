from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.CandidateRegisterView.as_view()),
    path("status/<int:pk>/", views.CandidateStatusView.as_view()),
    path("admin/candidates/", views.AdminListCandidatesView.as_view()),
    path("admin/candidates/<int:pk>/resume/", views.AdminResumeDownloadView.as_view()),
    path("admin/candidates/<int:pk>/status/", views.AdminUpdateStatusView.as_view()),
]
