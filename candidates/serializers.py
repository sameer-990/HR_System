from rest_framework import serializers
from .models import Candidate, ApplicationStatus
import os

import logging

logger = logging.getLogger('hr')


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ['application_status']

    def validate_resume(self, file):
        ext = os.path.splitext(file.name)[1]
        if ext not in ['.pdf', '.docx']:
            raise serializers.ValidationError("Only PDF or DOCX files are allowed.")
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File too large. Max 5MB.")
        return file

    def create(self, validated_data):
        resume = validated_data.pop('resume')
        candidate = Candidate.objects.create(**validated_data)
        candidate.resume.save(resume.name, resume)
        logger.info(f"Candidate registered: {candidate.full_name} (ID: {candidate.id})")
        return candidate


class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = ['status', 'updated_at', 'feedback', 'updated_by']


class CandidateStatusViewSerializer(serializers.ModelSerializer):
    statuses = StatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ['full_name', 'application_status', 'statuses']


class ListCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['full_name', 'date_of_birth', 'experience_years', 'department']
