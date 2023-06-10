import uuid
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import HTTPErrorDetails
from models.schemas.question import Question
from db.database import get_db
from services.questions import make_new, get_actual_q_session

router = APIRouter()


@router.post('/')
async def fetch_new_q(questions_num: int, db: AsyncSession = Depends(get_db)):
    q_session = await get_actual_q_session(db=db)
    return await make_new(count=questions_num, q_session=q_session, db=db)
