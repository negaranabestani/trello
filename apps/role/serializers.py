import traceback

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from dto_utils.response import BaseResponseDTO
from dto_utils.serilizer import ResponseDtoSerializer
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        read_only_fields = ['created_at', 'updated_at', 'id']
        fields = ['id', 'role', 'workspace', 'user', 'created_at', 'updated_at']

    def is_valid(self, *, raise_exception=False,**kwargs):
        print(kwargs)
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


class RoleResponseSerializer:
    def __init__(self, roles, message):
        self.roles = roles
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "roles": self.roles}
