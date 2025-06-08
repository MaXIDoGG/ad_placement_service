from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, utils
from auth.utils import get_current_active_user, get_active_admin_user
from models import get_session
from models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_active_admin_user)
):
    users = await utils.get_users(session, skip=skip, limit=limit)
    if not users:
      raise HTTPException(status_code=404, detail="Users not found")
    return users
  
@router.get("/me", response_model=schemas.UserBase, status_code=200)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return schemas.UserBase(login=current_user.login, name=current_user.name)
  
@router.post("/promote-to-admin/{user_id}", status_code=status.HTTP_200_OK)
async def promote_to_admin(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_active_admin_user)
):
    user_to_promote = await utils.promote_user_to_admin(session, user_id)
    
    return {
        "message": "User promoted to admin successfully",
        "user_id": user_to_promote.id,
        "login": user_to_promote.login
    }


@router.post("/ban/{user_id}", status_code=status.HTTP_200_OK)
async def ban_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_active_admin_user)
):
    user_to_promote = await utils.ban_user(session, user_id)
    
    return {
        "message": "User banned successfully",
        "user_id": user_to_promote.id,
        "login": user_to_promote.login
    }

@router.post("/unban/{user_id}", status_code=status.HTTP_200_OK)
async def unban_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_active_admin_user)
):
    user_to_promote = await utils.unban_user(session, user_id)
    
    return {
        "message": "User unbanned successfully",
        "user_id": user_to_promote.id,
        "login": user_to_promote.login
    }
