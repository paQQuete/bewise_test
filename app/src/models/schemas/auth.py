import uuid as builtin_uuid

from models.schemas.base import BaseSchemaModel, BaseFullModelMixin


class UserBase(BaseSchemaModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase, BaseFullModelMixin):
    uuid: builtin_uuid.UUID
    token: builtin_uuid.UUID

    class Config:
        orm_mode = True
