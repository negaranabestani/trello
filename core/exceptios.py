import datetime
import uuid

from rest_framework import status
from rest_framework.exceptions import APIException


class TrelloException(APIException):
    def __init__(self, detail, code=status.HTTP_400_BAD_REQUEST):
        detail = {
            "request_id": uuid.uuid4(),
            "message": detail,
            "data": None,
            "response_time": datetime.datetime.now()
        }
        super(TrelloException, self).__init__(detail, code)
