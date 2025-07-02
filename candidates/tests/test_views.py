from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from candidates.models import Candidate
from django.urls import reverse

class CandidateIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_candidate_success(self):
        resume = SimpleUploadedFile("cv.pdf", b"fakepdf", content_type="application/pdf")
        response = self.client.post(reverse("register_candidate"), {
            'full_name': 'Alice',
            'date_of_birth': '1990-01-01',
            'experience_years': 5,
            'department': 'HR',
            'email': 'x@x.com',
            'resume': resume
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Candidate.objects.filter(full_name="Alice").exists())

    def test_candidate_list_admin_access(self):
        # Create sample candidate
        Candidate.objects.create(
            full_name="Bob", date_of_birth="1980-01-01",
            experience_years=10, department="IT"
        )

        response = self.client.get(
            reverse("list_candidates"),
            HTTP_X_ADMIN="1"
        )

        self.assertContains(response, "Bob")
        self.assertEqual(response.status_code, 200)

    def test_candidate_list_without_admin_fails(self):
        response = self.client.get(reverse("list_candidates"))
        print(response.status_code)
        self.assertEqual(response.status_code, 403)

    def test_resume_download_admin_only(self):
        resume_file = SimpleUploadedFile("carol.pdf", b"resume content", content_type="application/pdf")

        candidate = Candidate.objects.create(
            full_name="Carol",
            date_of_birth="1985-01-01",
            experience_years=7,
            department="Finance",
            email='x@x.com',
            resume=resume_file
        )

        url = reverse("download_resume", args=[candidate.id])
        response = self.client.get(url, HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response.get("Content-Disposition", ""))

    def test_resume_download_unauthorized(self):
        candidate = Candidate.objects.create(
            full_name="Dave", date_of_birth="1985-01-01",
            experience_years=7, department="Finance"
        )
        candidate.resume.save("dave.pdf", SimpleUploadedFile("dave.pdf", b"resume"))

        response = self.client.get(reverse("download_resume", args=[candidate.id]))
        self.assertEqual(response.status_code, 403)
