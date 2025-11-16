from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet, DeadlineViewSet, FeedbackViewSet

router = DefaultRouter()
router.register('submissions', SubmissionViewSet)
router.register('deadlines', DeadlineViewSet)
router.register('feedbacks', FeedbackViewSet)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard_student/', views.dashboard_student, name='dashboard_student'),
    path('dashboard_faculty/', views.dashboard_faculty, name='dashboard_faculty'),
    path('upload_submission/', views.upload_submission, name='upload_submission'),
    path('feedback/<int:submission_id>/', views.feedback_view, name='feedback_view'),
]
urlpatterns += router.urls
