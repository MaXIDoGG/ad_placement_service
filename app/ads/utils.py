from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ad, User, Review
from typing import Union
from datetime import datetime
from fastapi import HTTPException, status

async def create_ad(session: AsyncSession, ad_data: dict, user: User):
    ad = Ad(**ad_data, created_at=datetime.now(), user_id=user.id)
    
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

async def get_ads(session: AsyncSession, skip: int = 0, limit: int = 100):
    result = await session.execute(select(Ad).offset(skip).limit(limit))
    return result.scalars().all()

async def get_ad_by_id(ad_id, session: AsyncSession) -> Union[Ad, None]:
    result = await session.execute(select(Ad).where(Ad.id==ad_id))
    return result.scalar_one_or_none()

async def del_ad(id:int, session: AsyncSession, user: User):
    result = await session.execute(select(Ad).filter_by(id=id, user_id=user.id))
    ad_to_delete = result.scalar_one_or_none()
    if not ad_to_delete:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Ad not found"
      )
    await session.execute(delete(Ad).filter_by(id=id, user_id=user.id))
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

async def get_reviews_by_ad_id(session: AsyncSession, ad_id: int):
    result = await get_ad_by_id(ad_id, session)
    if result is not None:
        return result.reviews
    else:
        return None

async def delete_review(session: AsyncSession, review_id, user_id):
    review = await get_review_by_id(session, review_id)
    if not review:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Review not found"
      )
    if review.user_id != user_id:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="You can only delete your review"
        )
    await session.execute(delete(Review).where(Review.id == review_id))
