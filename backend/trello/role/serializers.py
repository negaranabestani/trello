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

    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            self.initial_data['workspace']=1

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

    # def create(self, validated_data):
    #     raise_errors_on_nested_writes('create', self, validated_data)
    #
    #     ModelClass = self.Meta.model
    #
    #     # Remove many-to-many relationships from validated_data.
    #     # They are not valid arguments to the default `.create()` method,
    #     # as they require that the instance has already been saved.
    #     info = model_meta.get_field_info(ModelClass)
    #     many_to_many = {}
    #     for field_name, relation_info in info.relations.items():
    #         if relation_info.to_many and (field_name in validated_data):
    #             many_to_many[field_name] = validated_data.pop(field_name)
    #
    #     try:
    #         instance = ModelClass._default_manager.create(**validated_data)
    #     except TypeError:
    #         tb = traceback.format_exc()
    #         msg = (
    #             'Got a `TypeError` when calling `%s.%s.create()`. '
    #             'This may be because you have a writable field on the '
    #             'serializer class that is not a valid argument to '
    #             '`%s.%s.create()`. You may need to make the field '
    #             'read-only, or override the %s.create() method to handle '
    #             'this correctly.\nOriginal exception was:\n %s' %
    #             (
    #                 ModelClass.__name__,
    #                 ModelClass._default_manager.name,
    #                 ModelClass.__name__,
    #                 ModelClass._default_manager.name,
    #                 self.__class__.__name__,
    #                 tb
    #             )
    #         )
    #         raise TypeError(msg)
    #
    #     # Save many-to-many relationships after the instance is created.
    #     if many_to_many:
    #         for field_name, value in many_to_many.items():
    #             field = getattr(instance, field_name)
    #             field.set(value)
    #
    #
    #     return instance


class RoleResponseSerializer:
    def __init__(self, roles, message):
        self.roles = roles
        self.response = ResponseDtoSerializer(BaseResponseDTO(message)).data

    @property
    def data(self):
        return {"response": self.response, "workspaces": self.roles}
