from django.db import models


class TaskModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.title}"


class TaskStatusModel(models.Model):
    task = models.ForeignKey(
        TaskModel, on_delete=models.CASCADE, related_name="task_status"
    )
    assigned_to = models.UUIDField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("TODO", "TODO"),
            ("IN_PROGRESS", "IN_PROGRESS"),
            ("DONE", "DONE"),
        ],
        default="TODO",
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Task Status"
        verbose_name_plural = "Task Statuses"

    def __str__(self):
        return f"{self.pk} - {self.task.title} - {self.status}"
