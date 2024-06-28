import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str) and data.startswith('data:image'):
            # Format is data:image/png;base64,....
            _format, content = data.split(';base64,')
            ext = _format.split('/')[-1]  # Extract the image extension (e.g., png)

            # Generate a unique filename using uuid
            _id = uuid.uuid4()
            data = ContentFile(base64.b64decode(content), name=f'{_id}.{ext}')

        return super().to_internal_value(data)
