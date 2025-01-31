from graphene import relay
from tasks.types import TaskType, TaskStatusType


class TaskConnection(relay.Connection):
    class Meta:
        node = TaskType


class TaskStatusConnection(relay.Connection):
    class Meta:
        node = TaskStatusType
