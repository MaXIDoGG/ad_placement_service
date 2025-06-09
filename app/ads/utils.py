from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models import Ad, User, Review, Complaint
from typing import Optional, List, Union
from datetime import datetime
from fastapi import HTTPException, status

async def create_ad(session: AsyncSession, ad_data: dict, user: User) -> Ad:
    try:
        ad = Ad(
            **ad_data,
            created_at=datetime.now(),
            user_id=user.id
        )
        
        session.add(ad)
        await session.commit()
        await session.refresh(ad)
        return ad
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {str(e)}"
        )

async def get_ads(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Ad]:
    try:
        result = await session.execute(select(Ad).offset(skip).limit(limit))
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def get_ad_by_id(session: AsyncSession, ad_id: Union[int, None]) -> Optional[Ad]:
    try:
        result = await session.execute(select(Ad).where(Ad.id == ad_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def delete_ad(session: AsyncSession, ad_id: int, user: User) -> None:
    try:
        # First check if ad exists and belongs to user
        result = await session.execute(
            select(Ad).where(Ad.id == ad_id, Ad.user_id == user.id)
        )
        ad = result.scalar_one_or_none()
        
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ad not found or you don't have permission to delete it"
            )
            
        await session.execute(delete(Ad).where(Ad.id == ad_id))
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def create_review(session: AsyncSession, review_data: dict, user: User) -> Review:
    try:
        ad = await get_ad_by_id(session=session, ad_id=review_data.get("ad_id"))
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ad not found"
            )
            
        review = Review(
            **review_data,
            created_at=datetime.now(),
            user_id=user.id
        )
        
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {str(e)}"
        )
        
async def create_complaint(session: AsyncSession, complaint_data: dict, user: User) -> Review:
    try:
        ad = await get_ad_by_id(session=session, ad_id=complaint_data.get("ad_id"))
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ad not found"
            )
            
        complaint = Complaint(
            **complaint_data,
            created_at=datetime.now(),
            user_id=user.id
        )
        
        session.add(complaint)
        await session.commit()
        await session.refresh(complaint)
        return complaint
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {str(e)}"
        )

async def get_review_by_id(session: AsyncSession, review_id: int) -> Optional[Review]:
    try:
        return await session.get(Review, review_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def get_reviews_by_ad_id(session: AsyncSession, ad_id: int) -> Optional[List[Review]]:
    try:
        ad = await get_ad_by_id(session=session, ad_id=ad_id)
        return ad.reviews if ad else None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

async def get_complaints_by_ad_id(session: AsyncSession, ad_id: int) -> Optional[List[Complaint]]:
    try:
        ad = await get_ad_by_id(session=session, ad_id=ad_id)
        return ad.complaints if ad else None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


async def delete_review(session: AsyncSession, review_id: int, user: User) -> None:
    try:
        review = await get_review_by_id(session=session, review_id=review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
            
        if review.user_id != user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own reviews"
            )
            
        await session.execute(delete(Review).where(Review.id == review_id))
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )