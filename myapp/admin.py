from django.contrib import admin
from .models import EcoCategory, EcoAction, Upload, Reward, Redemption, Profile
from django.utils.html import format_html

class UploadInline(admin.TabularInline):
    model = Upload
    extra = 0
    readonly_fields = ('file_preview', 'uploaded_at')
    fields = ('file', 'file_preview')

    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_preview.short_description = 'Proof Preview'

@admin.action(description='Approve selected actions')
def approve_actions(modeladmin, request, queryset):
    for action in queryset:
        if action.status != 'Approved':
            action.status = 'Approved'
            action.save()
            profile = action.user.profile
            print(f"Before: {profile.points}")
            profile.points = profile.points + action.points
            profile.save()
            print(f"After: {profile.points}")

@admin.action(description='Reject selected actions')
def reject_actions(modeladmin, request, queryset):
    queryset.update(status='Rejected')

class EcoActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'points', 'date_logged')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'user__username')
    inlines = [UploadInline]
    actions = [approve_actions, reject_actions]

admin.site.register(EcoCategory)
admin.site.register(EcoAction, EcoActionAdmin)
admin.site.register(Upload)
admin.site.register(Reward)
admin.site.register(Redemption)
admin.site.register(Profile)
