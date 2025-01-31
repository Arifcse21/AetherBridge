import graphene
from graphene_django.types import DjangoObjectType
from tasks.models import TaskModel, TaskStatusModel


class TaskType(DjangoObjectType):
    class Meta:
        model = TaskModel
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        )
        interfaces = (graphene.relay.Node,)


class TaskStatusType(DjangoObjectType):
    class Meta:
        model = TaskStatusModel
        fields = (
            "id",
            "task",
            "assigned_to",
            "assigned_at",
            "status",
            "start_at",
            "end_at",
        )
        interfaces = (graphene.relay.Node,)
