from fastapi import Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Ad, User, Review
from datetime import datetime

async def get_users(session: AsyncSession, skip: int = 0, limit: int = 100):
    result = await session.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
  
async def promote_user_to_admin(session: AsyncSession, user_id):
  result = await session.execute(select(User).where(User.id == user_id))
  user_to_promote = result.scalar_one_or_none()
  
  if not user_to_promote:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="User not found"
      )

  if user_to_promote.is_admin:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="User is already an admin"
      )

  user_to_promote.is_admin = True
  await session.commit()
  await session.refresh(user_to_promote)
  return user_to_promote

async def ban_user(session: AsyncSession, user_id):
  result = await session.execute(select(User).where(User.id == user_id))
  user_to_ban = result.scalar_one_or_none()
  
  if not user_to_ban:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="User not found"
      )

  if user_to_ban.is_banned:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="User is already banned"
      )

  user_to_ban.is_banned = True
  await session.commit()
  await session.refresh(user_to_ban)
  return user_to_ban
  
  
async def unban_user(session: AsyncSession, user_id):
  result = await session.execute(select(User).where(User.id == user_id))
  user_to_ban = result.scalar_one_or_none()
  
  if not user_to_ban:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="User not found"
      )

  if not user_to_ban.is_banned:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="User is unbanned"
      )

  user_to_ban.is_banned = False
  await session.commit()
  await session.refresh(user_to_ban)
  return user_to_ban
    
