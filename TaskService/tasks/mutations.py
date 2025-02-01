import graphene
from tasks.models import TaskModel, TaskStatusModel
from tasks.types import TaskType, TaskStatusType


class CreateTaskInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()

    
class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        input = CreateTaskInput(required=True)

    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, input):
        task = TaskModel(**input)
        task.save()
        return CreateTaskMutation(task=task)
    
class UpdateTaskInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    title = graphene.String()
    description = graphene.String()


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        input = UpdateTaskInput(required=True)

    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, input):
        task = TaskModel.objects.filter(id=input.id)
        if not task.exists():
            raise Exception("Task not found")
        task = task.first()

        for field, value in input.items():
            if value is not None:
                setattr(task, field, value)

        task.save()

        return UpdateTaskMutation(task=task)


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, id):
        task = TaskModel.objects.filter(id=id)
        if not task.exists():
            raise Exception("Task not found")
        task = task.first()

        return task.delete()


class CreateTaskStatusInput(graphene.InputObjectType):
    task = graphene.ID(required=True)
    assigned_to = graphene.UUID(required=True)


class CreateTaskStatusMutation(graphene.Mutation):
    class Arguments:
        input = CreateTaskStatusInput(required=True)

    task_status = graphene.Field(TaskStatusType)

    def mutate(root, info, input):
        task_status = TaskStatusModel(**input)
        task_status.save()
        return CreateTaskStatusMutation(task_status=task_status)


class UpdateTaskStatusInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    assigned_to = graphene.UUID()
    status = graphene.String()
    start_at = graphene.DateTime()
    end_at = graphene.DateTime()


class UpdateTaskStatusMutation(graphene.Mutation):
    class Arguments:
        input = UpdateTaskStatusInput(required=True)

    task_status = graphene.Field(TaskStatusType)

    def mutate(root, info, input):
        task_status = TaskStatusModel.objects.filter(id=input.id)
        if not task_status.exists():
            raise Exception("TaskStatus not found")
        task_status = task_status.first()

        for field, value in input.items():
            if value is not None:
                setattr(task_status, field, value)

        task_status.save()

        return UpdateTaskStatusMutation(task_status=task_status)
    

class DeleteTaskStatusMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    task_status = graphene.Field(TaskStatusType)

    def mutate(root, info, id):
        task_status = TaskStatusModel.objects.filter(id=id)
        if not task_status.exists():
            raise Exception("TaskStatus not found")
        task_status = task_status.first()

        return task_status.delete()
