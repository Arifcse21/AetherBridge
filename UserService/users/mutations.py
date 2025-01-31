import graphene
from users.models import UserModel
from users.types import UserType


class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    address = graphene.String()
    phone = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, input):
        user = UserModel.objects.create_user(**input)
        return CreateUserMutation(user=user)


class UpdateUserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    username = graphene.String()
    email = graphene.String()
    address = graphene.String()
    phone = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        input = UpdateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, input):
        user = UserModel.objects.filter(id=input.id)
        if not user.exists():
            raise Exception("User not found")
        user = user.first()

        for field, value in input.items():
            if value is not None:
                setattr(user, field, value)

        user.save()
        return UpdateUserMutation(user=user)


class DeleteUserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        input = DeleteUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, input):
        user = UserModel.objects.filter(id=input.id)
        if not user.exists():
            raise Exception("User not found")
        user = user.first()

        return user.delete()
