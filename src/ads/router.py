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
async def read_ads(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await utils.get_ads(session, skip=skip, limit=limit)

@router.get("/del_ad", status_code=200)
async def delete_ad(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    await utils.del_ad(id, session, current_user)
    return {"info": "Successfully delete."}

@router.post("/create_review", status_code=201)
async def create_review(
    review: schemas.ReviewBase,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    return await utils.create_review(session, review.model_dump(), current_user)

@router.get("/get_review_by_id/{review_id}", response_model=schemas.Review)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session)
):
    review = await utils.get_review_by_id(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
