from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    def __str__(self):
        return self.name

class Deadline(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='deadlines')
    def __str__(self):
        return f"{self.title} for {self.team}"

class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='submissions')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='mini_projects/')
    deadline = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Submitted')
    def __str__(self):
        return f"Submission by {self.team} for {self.deadline.title}"

class Feedback(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='feedback')
    comments = models.TextField()
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_at = models.DateTimeField(auto_now_add=True)
