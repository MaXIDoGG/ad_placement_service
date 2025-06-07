from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ad
from models import User
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

async def del_ad(session: AsyncSession, id:int):
    ad = await session.execute(delete(Ad).filter_by(id=id))
    await session.commit()
    
