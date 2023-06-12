from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.models import HTTPErrorDetails
from models.schemas.auth import UserCreate, User
from db.database import get_db
from services.auth import create_user as user_create_service

router = APIRouter()


@router.post('/register/', response_model=User)
async def create_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await user_create_service(user_info=user_create, db=db)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=HTTPErrorDetails.CONFLICT.value)
    else:
        return user


