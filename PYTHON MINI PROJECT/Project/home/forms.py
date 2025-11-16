from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Submission, Feedback

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('file', 'deadline', 'team')
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('comments',)
