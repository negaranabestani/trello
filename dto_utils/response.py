import datetime
import uuid

class BaseResponseDTO:
    def __init__(self, message):
        self.message = message
        self.response_time = datetime.datetime.now()
        self.response_ID = uuid.uuid4()
