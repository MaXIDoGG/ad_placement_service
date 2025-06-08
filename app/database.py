from models.base import Base, engine, async_session
from auth.utils import get_password_hash
from sqlalchemy import select
from models.user import *
from models.ad import *
from config import ADMIN_LOGIN, ADMIN_NAME, ADMIN_PASSWORD

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def create_admin():
    session = async_session()
    result = await session.execute(select(User).where(User.login==ADMIN_LOGIN))
    admin = result.first()
    if not admin:
        new_admin = User(
            login=ADMIN_LOGIN,
            name=ADMIN_NAME,
            password_hash = get_password_hash(ADMIN_PASSWORD),
            is_admin = True
        )
        session.add(new_admin)
        await session.commit()