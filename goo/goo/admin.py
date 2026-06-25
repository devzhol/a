from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .mixins import ProfileAdminSummaryMixin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(ProfileAdminSummaryMixin, UserAdmin):
    list_display = (
        'username',
        'email',
        'profile_summary',
        'phone_number',
        'city',
        'birth_date',
        'receive_newsletter',
    )
    list_filter = ('receive_newsletter', 'city')
    search_fields = ('username', 'email', 'phone_number', 'city')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
            'fields': (
                'bio',
                'phone_number',
                'birth_date',
                'city',
                'website',
                'receive_newsletter',
            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('email',),
        }),
    )

    def get_list_display(self, request):
        self.profile_summary.short_description = self.profile_summary_label
        return super().get_list_display(request)
