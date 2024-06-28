from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        read_only_fields = ['created_at', 'updated_at', 'id', 'task', 'assignee']
        fields = ['id', 'title', 'task', 'assignee', 'created_at', 'updated_at']

    def is_valid(self, *, raise_exception=False, **kwargs):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            self.initial_data['task'] = kwargs['kwargs'].get("task")

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


class SubTaskResponseSerializer:
    def __init__(self, tasks, message):
        self.tasks = tasks
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "subtasks": self.tasks}
