from graphene import relay
from users.types import UserType


class UserConnection(relay.Connection):
    class Meta:
        node = UserType
