from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ad, User, Review
from datetime import datetime

async def create_ad(session: AsyncSession, ad_data: dict, user: User):
    ad = Ad(**ad_data, created_at=datetime.now(), user_id=user.id)
    
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

async def get_ads(session: AsyncSession, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Ad).offset(skip).limit(limit))
    return result.scalars().all()

async def del_ad(id:int, session: AsyncSession, user: User):
    ad = await session.execute(delete(Ad).filter_by(id=id, user_id=user.id))
    await session.commit()
    

async def create_review(session: AsyncSession, review_data: dict, user: User):
    review = Review(**review_data, created_at=datetime.now(), user_id=user.id)
    
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review

async def get_review_by_id(session: AsyncSession, review_id: int):
    result = await session.get(Review, review_id)
    return result