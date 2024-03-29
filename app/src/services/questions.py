import datetime
import uuid

import aiohttp
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Questions
from core.config import SETTINGS, ApiTypesURI


async def _fetch(count: int, path: str = SETTINGS.Q_API) -> list[dict]:
    """Fetch new questions from provided public API"""
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url=f"{path}{ApiTypesURI.RANDOM.value}?count={count}"
        )
    return await response.json(encoding='UTF-8')


async def get_actual_q_session(db: AsyncSession) -> int:
    """Get number of actual query session"""
    last_query_session = await db.execute(select(func.max(Questions.query_session)))
    last_query_session = last_query_session.scalar()
    if last_query_session is None:
        return 1
    else:
        return last_query_session + 1


async def make_new(count: int, q_session: int, db: AsyncSession) -> list[dict]:
    """Create entries for every fetched question from public API, if questions already exist in database -
    try to fetch new questions, until provided count (query for new questions) equals to fetch new questions"""
    new_count = 0
    for question in await _fetch(count=count):
        exists_q = await db.execute(select(Questions).where(Questions.id == question['id']))
        exists_q = exists_q.scalar()
        if exists_q is None:
            new_question = Questions(
                uuid=uuid.uuid4(),
                id=question.get('id'),
                question=question.get('question'),
                answer=question.get('answer'),
                question_created_at=datetime.datetime.fromisoformat(question['created_at']),
                query_session=q_session,
            )
            db.add(new_question)
            await db.flush()
        else:
            new_count += 1
    if new_count:
        await make_new(count=new_count, q_session=q_session, db=db)
    else:

        prev_query_session = await db.execute(
            select(Questions).where(Questions.query_session == q_session - 1))
        await db.commit()
        return prev_query_session.scalars().all()
