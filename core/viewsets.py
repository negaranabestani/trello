import datetime
import uuid

from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.exceptios import TrelloException


class BaseViewSet(ModelViewSet):
    def get_permissions(self):
        return [IsAuthenticated(), ]

    def permission_denied(self, request, message=None, code=None):
        if not message:
            raise TrelloException("ابتدا وارد سیستم شوید.", code=403)
        super(BaseViewSet, self).permission_denied(request, message=None, code=None)

    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super(BaseViewSet, self).dispatch(request, *args, **kwargs)
        if str(response.status_code).startswith("2"):
            response.data = {
                "request_id": uuid.uuid4(),
                "message": "عملیات با موفقیت انجام شد.",
                "response_time": datetime.datetime.now(),
                "data": response.data
            }
        return response
