from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['created_at', 'updated_at', 'id', 'workspace', 'assignee']
        fields = ['id', 'title', 'workspace', 'assignee', 'created_at', 'updated_at', 'description',
                  'estimated_time', 'actual_time', 'due_date', 'priority', 'status', 'image_url']

    def is_valid(self, *, raise_exception=False, **kwargs):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            self.initial_data['workspace'] = kwargs['kwargs'].get("workspace")

            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)


class TaskResponseSerializer:
    def __init__(self, tasks, message):
        self.tasks = tasks
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "tasks": self.tasks}
