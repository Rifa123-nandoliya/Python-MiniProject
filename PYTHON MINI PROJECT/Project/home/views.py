from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from .models import Team, Submission, Deadline, Feedback, User
from .forms import UserRegisterForm, SubmissionForm, FeedbackForm
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TeamSerializer, SubmissionSerializer, DeadlineSerializer, FeedbackSerializer
from .permissions import IsStudent, IsFaculty

# HTML-based views

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'home/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('dashboard_student')
            else:
                return redirect('dashboard_faculty')
        else:
            return render(request, 'home/login.html', {"error": "Invalid credentials"})
    return render(request, 'home/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_student(request):
    deadlines = Deadline.objects.filter(team__in=request.user.teams.all()).order_by('due_date')
    submissions = Submission.objects.filter(uploaded_by=request.user)
    return render(request, 'home/dashboard_student.html', {'deadlines': deadlines, 'submissions': submissions})

@login_required
def dashboard_faculty(request):
    teams = Team.objects.all()
    submissions = Submission.objects.select_related('team', 'deadline').all()
    # Progress bar calculation per team
    progress = []
    for team in teams:
        total = team.deadlines.count()
        submitted = Submission.objects.filter(team=team, deadline__in=team.deadlines.all()).count()
        pct = int(100 * submitted / total) if total else 0
        progress.append({'team': team, 'pct': pct})
    return render(request, 'home/dashboard_faculty.html', {'teams': teams, 'progress': progress, 'submissions': submissions})

@login_required
def upload_submission(request):
    if request.user.role != 'student':
        return redirect('dashboard_student')
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            deadline = submission.deadline
            if timezone.now() > deadline.due_date:
                form.add_error('file', 'Deadline has passed!')
            else:
                submission.uploaded_by = request.user
                submission.save()
                return redirect('dashboard_student')
    else:
        form = SubmissionForm()
    return render(request, 'home/submission_upload.html', {'form': form})

@login_required
def feedback_view(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if request.user.role != 'faculty':
        return redirect('dashboard_student')
    try:
        feedback = submission.feedback
        form = FeedbackForm(instance=feedback)
    except Feedback.DoesNotExist:
        form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb, created = Feedback.objects.update_or_create(submission=submission, defaults={
                'comments': form.cleaned_data['comments'],
                'reviewed_by': request.user
            })
            return redirect('dashboard_faculty')
    return render(request, 'home/feedback.html', {'form': form, 'submission': submission})

# --- DRF API views ---
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    def perform_create(self, serializer):
        deadline = serializer.validated_data['deadline']
        if timezone.now() > deadline.due_date:
            raise serializers.ValidationError("Cannot submit after the deadline.")
        serializer.save(uploaded_by=self.request.user)
    def get_permissions(self):
        if self.action in ['create']:
            return [IsStudent()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsFaculty()]
        return [permissions.IsAuthenticated()]
    @action(detail=False, methods=['get'], permission_classes=[IsFaculty])
    def progress(self, request):
        teams = Team.objects.all()
        data = []
        for team in teams:
            total = team.deadlines.count()
            submitted = team.submissions.filter(deadline__in=team.deadlines.all()).count()
            pct = int(100 * submitted / total) if total else 0
            data.append({
                "team": team.name,
                "progress": pct
            })
        return Response(data)

class DeadlineViewSet(viewsets.ModelViewSet):
    queryset = Deadline.objects.all()
    serializer_class = DeadlineSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFaculty()]
        return [permissions.IsAuthenticated()]
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def get_permissions(self):
        if self.action in ['create']:
            return [IsFaculty()]
        return [permissions.IsAuthenticated()]
