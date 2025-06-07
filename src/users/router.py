from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from auth.utils import get_current_active_user
from auth.schemas import UserCreate


router = APIRouter()

@router.get("/users/me/", response_model=UserCreate)
async def read_users_me(
    current_user: Annotated[UserCreate, Depends(get_current_active_user)],
):
    return current_user