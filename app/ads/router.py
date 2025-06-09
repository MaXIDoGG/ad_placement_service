from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from . import schemas, utils
from auth.utils import get_current_active_user
from models import get_session
from models import User

router = APIRouter(prefix="/ads", tags=["ads"])

@router.post("/", response_model=schemas.Ad, status_code=status.HTTP_201_CREATED)
async def create_ad(
    ad: schemas.AdCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return await utils.create_ad(session=session, ad_data=ad.model_dump(), user=current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ad: {str(e)}"
        )

@router.get("/", response_model=List[schemas.Ad])
async def get_ads(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    if limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot fetch more than 1000 items at once"
        )
    
    try:
        return await utils.get_ads(session=session, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch ads: {str(e)}"
        )

@router.get("/{ad_id}", response_model=schemas.Ad)
async def get_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_session)
):
    ad = await utils.get_ad_by_id(session=session, ad_id=ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad not found"
        )
    return ad

@router.delete("/{ad_id}")
async def delete_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        await utils.delete_ad(session=session, ad_id=ad_id, user=current_user)
        return {"detail": "Ad successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete ad: {str(e)}"
        )

## Reviews ##
@router.get("/{ad_id}/reviews", response_model=List[schemas.Review])
async def get_reviews_by_ad_id(
    ad_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        reviews = await utils.get_reviews_by_ad_id(session=session, ad_id=ad_id)
        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No reviews found for this ad"
            )
        return reviews
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch reviews: {str(e)}"
        )

@router.post("/{ad_id}/reviews", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
async def create_review(
    ad_id: int,
    review: schemas.ReviewCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Check if ad exists
        ad = await utils.get_ad_by_id(session=session, ad_id=ad_id)
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ad not found"
            )
            
        review_data = review.model_dump()
        review_data["ad_id"] = ad_id
        return await utils.create_review(session=session, review_data=review_data, user=current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create review: {str(e)}"
        )

@router.get("/reviews/{review_id}", response_model=schemas.Review)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session)
):
    review = await utils.get_review_by_id(session=session, review_id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review

@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        await utils.delete_review(session=session, review_id=review_id, user_id=current_user.id)
        return {"detail": "Review successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete review: {str(e)}"
        )