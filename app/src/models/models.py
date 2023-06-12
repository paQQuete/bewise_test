import datetime
import uuid
import enum

from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey, Float, Boolean, Index
from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy.orm import relationship

from db.database import Base


class DefaultMixin:
    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class HTTPErrorDetails(enum.Enum):
    NOT_FOUND = 'Not found this entity'
    NOT_ACCEPTABLE = 'This operation is not available for this entity'
    UNPROCESSABLE_ENTITY = 'This entity cannot be processed'
    BAD_REQUEST = 'Invalid data provided'
    CONFLICT = 'Provided data already exists'
    UNAUTHORIZED = 'You are not authorized for this request'


class Questions(DefaultMixin, Base):
    __tablename__ = 'questions'
    __table_args__ = {'schema': 'content'}

    id = Column(Integer, nullable=False, index=True, unique=True)
    question = Column(String(length=255), nullable=False)
    answer = Column(String(length=255), nullable=False)
    question_created_at = Column(DateTime(timezone=True), nullable=False)
    query_session = Column(Integer, nullable=False, index=True)


class Users(DefaultMixin, Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'content'}

    username = Column(String(length=50), nullable=False, index=True, unique=True)
    token = Column(UUIDType(binary=False), nullable=False, unique=True)

    audiofile = relationship('AudioFiles', back_populates='user', foreign_keys='AudioFiles.user_uuid')


class AudioFiles(DefaultMixin, Base):
    __tablename__ = 'audiofiles'
    __table_args__ = {'schema': 'content'}

    wav_file = Column(String(length=255), nullable=True, unique=True)
    mp3_file = Column(String(length=255), nullable=True, unique=True)
    user_uuid = Column(UUIDType(binary=False), ForeignKey('content.users.uuid'), nullable=False, unique=False)

    user = relationship('Users', back_populates='audiofile', foreign_keys=user_uuid)


