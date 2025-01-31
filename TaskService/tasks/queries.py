import graphene
from graphene import relay
from django.db.models import Q
from graphene_django import DjangoObjectType
from tasks.connections import *
from tasks.types import *
from tasks.models import *


class TaskQuery(graphene.ObjectType):
    all_tasks = relay.ConnectionField(
        TaskConnection,
        search=graphene.String(),
        order_by=graphene.String(),
    )
    task = graphene.Field(TaskType, id=graphene.ID(required=True))

    def resolve_all_tasks(self, info, search=None, order_by="id", **kwargs):
        all_tasks = TaskModel.objects.all().order_by(order_by)
        if search:
            all_tasks = all_tasks.filter(
                Q(title__contains=search)
                | Q(description__icontains=search)
            )
        return all_tasks

    def resolve_task(self, info, id, **kwargs):
        task = TaskModel.objects.filter(id=id)
        if not task.exists():
            raise Exception("Task not found")
        return task.first()
