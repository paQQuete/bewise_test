import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Users as UserModel
from models.schemas.auth import UserCreate


async def create_user(user_info: UserCreate, db: AsyncSession) -> UserModel:
    """Create user"""
    db_user = UserModel(**user_info.dict())
    db_user.token = uuid.uuid4()
    db.add(db_user)
    await db.flush()
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_uuid(user_uuid: uuid.UUID, db: AsyncSession) -> UserModel | None:
    """Get user by id, return None if user with provided id does not exist"""
    exists_user = await db.execute(select(UserModel).where(UserModel.uuid == user_uuid))
    exists_user = exists_user.scalar()
    if exists_user:
        return exists_user
    else:
        return None


async def get_user_by_token(user_token: uuid.UUID, db: AsyncSession) -> UserModel | None:
    """Get user by unique token, return None if user with provided id does not exist"""
    exists_user = await db.execute(select(UserModel).where(UserModel.token == user_token))
    exists_user = exists_user.scalar()
    if exists_user:
        return exists_user
    else:
        return None
