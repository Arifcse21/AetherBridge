import graphene
from graphene_django.types import DjangoObjectType
from users.models import UserModel


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
            "is_active",
        )
        interfaces = (graphene.relay.Node,)
