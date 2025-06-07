from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import Token, UserBase, UserCreate
from .utils import authenticate_user, create_access_token, get_current_active_user, get_user, get_password_hash
from models.base import get_session
from models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post("/token")
@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserBase, status_code=200)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return UserBase(login=current_user.login, name=current_user.name)

@router.post("/register", status_code=201)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    existing_user = await get_user(session, user_data.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        login=user_data.login,
        name=user_data.name,
        password_hash=hashed_password,
    )
    
    session.add(new_user)
    await session.commit()


