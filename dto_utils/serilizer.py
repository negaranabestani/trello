from rest_framework import serializers
class ResponseDtoSerializer(serializers.Serializer):
    response_time = serializers.DateTimeField()
    response_ID = serializers.CharField()
    message = serializers.CharField()
