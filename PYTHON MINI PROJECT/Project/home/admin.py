from django.contrib import admin
from .models import User, Team, Deadline, Submission, Feedback
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Deadline)
admin.site.register(Submission)
admin.site.register(Feedback)

# Register your models here.
