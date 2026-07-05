from django.contrib import admin
from .models import Topic, Plan, Tasks

class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'field']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Plan)
admin.site.register(Tasks)

