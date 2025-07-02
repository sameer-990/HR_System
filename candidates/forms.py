from django import forms
from candidates.models import Candidate

class CandidateRegistrationForm(forms.ModelForm):
    resume = forms.FileField(required=True)

    class Meta:
        model = Candidate
        fields = ['full_name', 'date_of_birth', 'experience_years', 'department', 'resume', 'email']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if resume:
            ext = resume.name.split('.')[-1].lower()
            allowed_ext = ['pdf', 'docx']
            if ext not in allowed_ext:
                raise forms.ValidationError("Resume must be a PDF or DOCX file.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file size must be under 5MB.")

        return resume
