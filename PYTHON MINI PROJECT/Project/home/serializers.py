from rest_framework import serializers
from .models import User, Team, Deadline, Submission, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'email')

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ('id', 'name', 'members')

class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = ('id', 'title', 'description', 'due_date', 'team')

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'team', 'uploaded_by', 'file', 'deadline', 'submitted_at', 'status')
        read_only_fields = ('uploaded_by', 'submitted_at', 'status')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'submission', 'comments', 'reviewed_by', 'reviewed_at')
        read_only_fields = ('reviewed_by', 'reviewed_at')
