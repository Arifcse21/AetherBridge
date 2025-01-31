import graphene
from graphene_federation import build_schema as make_federated_schema

from users.mutations import CreateUserMutation, UpdateUserMutation, DeleteUserMutation
from users.queries import UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()


schema = make_federated_schema(Query, Mutation)
