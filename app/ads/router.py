from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, utils
from auth.utils import get_current_active_user
from models import get_session
from models import User

router = APIRouter(prefix="/ads", tags=["ads"])

@router.post("/", response_model=schemas.Ad)
async def create_ad(
    ad: schemas.AdCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    return await utils.create_ad(session, ad.model_dump(), current_user)

@router.get("/", response_model=list[schemas.Ad])
async def get_ads(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await utils.get_ads(session, skip=skip, limit=limit)

@router.get("/{ad_id}", response_model=schemas.Ad)
async def get_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await utils.get_ad_by_id(ad_id, session)


@router.delete("/{ad_id}", status_code=200)
async def delete_ad(
    ad_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    await utils.del_ad(ad_id, session, current_user)
    return {"info": "Successfully delete."}
   


## Reviews ##
@router.get("/{ad_id}/reviews", response_model=list[schemas.Review])
async def get_reviews_by_ad_id(
    ad_id: int,
    session: AsyncSession = Depends(get_session)
):
    reviews = await utils.get_reviews_by_ad_id(session, ad_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews

@router.post("/{ad_id}/reviews", status_code=201)
async def create_review(
    review: schemas.ReviewCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    return await utils.create_review(session, review.model_dump(), current_user)

@router.get("/reviews/{review_id}", response_model=schemas.Review)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session)
):
    review = await utils.get_review_by_id(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.delete("/reviews/{review_id}", status_code=201)
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    return await utils.delete_review(session, review_id, current_user.id)