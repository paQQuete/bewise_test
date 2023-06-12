from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from services.questions import make_new, get_actual_q_session

router = APIRouter()


@router.post('/')
async def fetch_new_q(questions_num: int, db: AsyncSession = Depends(get_db)):
    """
    Function get actual session id and start fetch process
    :param questions_num: count for fetch new questions
    :param db:
    :return: questions from previously query session
    """
    q_session = await get_actual_q_session(db=db)
    return await make_new(count=questions_num, q_session=q_session, db=db)
