import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.models import HTTPErrorDetails
from db.database import get_db
from services import balance_r

router = APIRouter()

@router.get('/')
async def test(value: str, db: AsyncSession = Depends(get_db)):
    return {'value': value}
