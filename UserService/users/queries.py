import graphene
from graphene import relay
from django.db.models import Q
from graphene_django import DjangoObjectType
from users.connections import UserConnection
from users.types import UserType
from users.models import UserModel


class UserQuery(graphene.ObjectType):
    all_users = relay.ConnectionField(
        UserConnection,
        search=graphene.String(),
        order_by=graphene.String(),
    )
    user = graphene.Field(UserType, id=graphene.ID(required=True))

    def resolve_all_users(self, info, search=None, order_by="id", **kwargs):
        all_users = UserModel.objects.all().order_by(order_by)
        if search:
            all_users = all_users.filter(
                Q(username__icontains=search)
                | Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )
        return all_users

    def resolve_user(self, info, id, **kwargs):
        user = UserModel.objects.filter(id=id)
        if not user.exists():
            raise Exception("User not found")
        return user.first()
