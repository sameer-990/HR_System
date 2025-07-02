from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Candidate, ApplicationStatus
from .serializers import CandidateSerializer, CandidateStatusViewSerializer, ListCandidateSerializer
from django.shortcuts import render
from candidates.forms import CandidateRegistrationForm
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, HttpResponseForbidden

import logging

logger = logging.getLogger('hr')

from django.core.mail import send_mail


def send_status_update_notification(candidate, status, feedback):
    if not candidate.email:
        return
    subject = f"Application Status Updated: {status}"
    message = f"Dear {candidate.full_name},\n\n" \
              f"Your application status is now: {status}.\n" \
              f"Feedback: {feedback}\n\n" \
              "Thank you,\nHR Team"

    send_mail(
        subject,
        message,
        from_email=None,
        recipient_list=[candidate.email],
    )


item_per_page = 20


class AdminPagination(PageNumberPagination):
    page_size = item_per_page


class CandidateRegisterView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


class CandidateStatusView(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateStatusViewSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]


class AdminListCandidatesView(generics.ListAPIView):
    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = ListCandidateSerializer
    pagination_class = AdminPagination
    ordering_fields = ["created_at"]
    filterset_fields = ["department"]

    def get_queryset(self):
        if self.request.headers.get("X-ADMIN") != "1":
            return Candidate.objects.none()
        qs = Candidate.objects.all().order_by('-created_at')
        dept = self.request.query_params.get('department')
        if dept:
            qs = qs.filter(department=dept)
        return qs


class AdminUpdateStatusView(APIView):
    def post(self, request, pk):
        if request.headers.get("X-ADMIN") != "1":
            return Response({'detail': 'Unauthorized'}, status=403)

        candidate = get_object_or_404(Candidate, pk=pk)
        new_status = request.data.get("status")
        feedback = request.data.get("feedback", "")
        updated_by = "Admin"

        if new_status not in dict(Candidate.STATUS_CHOICES).keys():
            return Response({'detail': 'Invalid status'}, status=400)

        candidate.application_status = new_status
        candidate.save()

        ApplicationStatus.objects.create(
            candidate=candidate,
            status=new_status,
            feedback=feedback,
            updated_by=updated_by
        )
        logger.info(
            f"Status updated: Candidate {candidate.id} to '{new_status}' "
            f"by Admin. Feedback: {feedback}"
        )
        send_status_update_notification(candidate, new_status, feedback)
        return Response({'detail': 'Status updated'})


class AdminResumeDownloadView(APIView):
    def get(self, request, pk):
        if request.headers.get("X-ADMIN") != "1":
            logger.warning(f"Unauthorized download attempt for Candidate ID {pk}")
            return Response({'detail': 'Unauthorized'}, status=403)

        candidate = get_object_or_404(Candidate, pk=pk)
        if not candidate.resume:
            logger.error(f"Resume not found for Candidate ID {pk}")
            raise Http404("Resume not found")
        try:
            logger.info(f"Resume downloaded for Candidate ID {pk} by Admin")
            return FileResponse(candidate.resume.open(), as_attachment=True)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


def register_candidate(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'register_candidate.html', {
                'form': CandidateRegistrationForm(),  # empty form after success
                'message': 'Registration successful!',
                'error': False,
            })
    else:
        form = CandidateRegistrationForm()

    return render(request, 'register_candidate.html', {'form': form})


def list_candidates_view(request):
    is_admin = request.headers.get("X-ADMIN") == "1"
    if request.headers.get("X-ADMIN") != "1":
        return render(request, "not_authorized.html", status=403)

    department = request.GET.get("department")
    page_number = request.GET.get("page", 1)

    candidates = Candidate.objects.all().order_by("-created_at")

    if department in ['IT', 'HR', 'Finance']:
        candidates = candidates.filter(department=department)

    paginator = Paginator(candidates, item_per_page)  # 25 per page
    page = paginator.get_page(page_number)

    return render(request, "list_candidates.html", {
        "page": page,
        "departments": ['IT', 'HR', 'Finance'],
        "selected_department": department,
        "is_admin": is_admin,
    })


def download_resume_view(request, pk):
    if request.headers.get("X-ADMIN") != "1":
        return HttpResponseForbidden("Unauthorized")

    candidate = get_object_or_404(Candidate, pk=pk)

    if not candidate.resume:
        raise Http404("Resume not found")

    return FileResponse(candidate.resume.open(), as_attachment=True)
