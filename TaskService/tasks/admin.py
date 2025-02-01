from django.contrib import admin
from tasks.models import TaskModel, TaskStatusModel

@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
    # list_per_page = 10

@admin.register(TaskStatusModel)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at", "updated_at")
    # list_per_page = 10
