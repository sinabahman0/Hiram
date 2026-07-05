from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserRelationship


class UserAdmin(BaseUserAdmin):

    list_display = ['username', 'first_name', 'last_name', 'user_type', 'is_active']
    list_filter = ['user_type', 'date_joined']
    list_editable = ['is_active']
    search_fields = ['username', 'first_name', 'last_name']
    actions = ['make_student', 'make_admin', 'make_advisor']

    def make_student(self, request, queryset):
        queryset.update(user_type='student')

    make_student.short_description = 'تغییر نقش به دانش‌اموز'

    def make_admin(self, request, queryset):
        queryset.update(user_type='admin')

    make_admin.short_description = 'تغییر نقش به ادمین'

    def make_advisor(self, request, queryset):
        queryset.update(user_type='advisor')

    make_advisor.short_description = 'تغییر نقش به مشاور'


class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ['student', 'admin', 'advisor']


admin.site.register(User, UserAdmin)
admin.site.register(UserRelationship, UserRelationshipAdmin)
