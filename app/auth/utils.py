from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import bcrypt
import jwt
from .schemas import TokenData, UserCreate
from models import User, get_session
from config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def get_user(session: AsyncSession, login: str) -> User:
    result = await session.execute(select(User).where(User.login == login))
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(session: AsyncSession, login: str, password: str):
    user = await get_user(session, login)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(session, login=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_banned:
        raise HTTPException(status_code=400, detail="Banned user")
    return current_user


async def get_active_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_banned:
        raise HTTPException(status_code=400, detail="Banned user")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="User isn't admin")
    return current_user

async def create_new_user(user_data: UserCreate, session: AsyncSession):
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
    return new_user