import graphene
from graphene_federation import build_schema as make_federated_schema

from tasks.mutations import *
from tasks.queries import *


class Query(
    TaskQuery,
    TaskStatusQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    create_task = CreateTaskMutation.Field()
    update_task = UpdateTaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()

    create_task_status = CreateTaskStatusMutation.Field()
    update_task_status = UpdateTaskStatusMutation.Field()
    delete_task_status = DeleteTaskStatusMutation.Field()


schema = make_federated_schema(Query, Mutation)
