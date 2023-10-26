import datetime
from typing import Literal
from bson import ObjectId as _ObjectId

from pydantic import BaseModel, AfterValidator
from typing_extensions import Annotated


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id), ]


class CreateNote(BaseModel):
    user_id: ObjectId
    target_id: ObjectId = None
    key: Literal["registration", "new_message", "new_post", "new_login"]
    data: dict = None


class Notification(BaseModel):
    id: ObjectId = None
    timestamp: int | None = int(datetime.datetime.utcnow().timestamp())
    key: Literal["registration", "new_message", "new_post", "new_login"]
    is_new: bool = True
    user_id: ObjectId
    target_id: ObjectId | None = None
    data: dict | None = dict()



