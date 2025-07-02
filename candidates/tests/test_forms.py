from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from candidates.forms import CandidateRegistrationForm
import io


class CandidateFormTests(TestCase):
    def test_valid_resume_pdf(self):
        form = CandidateRegistrationForm(data={
            'full_name': 'Test User',
            'date_of_birth': '2000-01-01',
            'experience_years': 3,
            'department': 'IT',
            'email': 'xx@xx.com'
        }, files={
            'resume': SimpleUploadedFile('resume.pdf', b'%PDF-1.4', content_type='application/pdf')
        })
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_file_extension(self):
        form = CandidateRegistrationForm(data={
            'full_name': 'Test User',
            'date_of_birth': '2000-01-01',
            'experience_years': 3,
            'department': 'IT',
            'email': 'xx@xx.com'
        }, files={
            'resume': SimpleUploadedFile('resume.txt', b'Some text', content_type='text/plain')
        })

        self.assertFalse(form.is_valid())
        self.assertIn('resume', form.errors)

    def test_file_size_limit(self):
        big_file = SimpleUploadedFile('resume.pdf', b'x' * (6 * 1024 * 1024), content_type='application/pdf')  # 6MB
        form = CandidateRegistrationForm(data={
            'full_name': 'Test User',
            'date_of_birth': '2000-01-01',
            'experience_years': 3,
            'department': 'IT',
            'email': 'xx@xx.com'
        }, files={'resume': big_file})

        self.assertFalse(form.is_valid())
        self.assertIn('resume', form.errors)
