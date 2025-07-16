
from .models import ContactMessage
from .models import CustomUser
from django.contrib import admin
from .models import CustomUser, TeamMember, Service, Feedback

from .models import ConsultationRequest

@admin.register(ConsultationRequest)
class ConsultationAdmin(admin.ModelAdmin):
    list_display  = ("name", "email", "service", "created","email_sent")   # ← replaced ‘submitted’
    list_filter   = ("service", "created","email_sent")                    # ← replaced ‘submitted’
    search_fields = ("name", "email", "service")
    ordering      = ("-created",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon']
    search_fields = ['title']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('rating', 'message', 'user', 'submitted_at')
    list_filter = ('rating', 'submitted_at')
    search_fields = ('message', 'user__username')



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')

# myapp/admin.py

# myapp/admin.py  (add)
from .models import PricingPlan

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan_type', 'price', 'is_popular')
    list_filter = ('plan_type', 'is_popular')
    search_fields = ('title', 'description')
