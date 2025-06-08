from models import async_session, User
from sqlalchemy import select
from auth.utils import get_password_hash
import asyncio
from config import ADMIN_LOGIN, ADMIN_NAME, ADMIN_PASSWORD
session = async_session()

async def create_admin():
  result = await session.execute(select(User).where(User.login=="admin"))
  admin = result.first()
  if not admin:
    new_admin = User(
      login="admin",
      name="admin",
      password_hash = get_password_hash("admin"),
      is_admin = True
    )
    session.add(new_admin)
    await session.commit()
 
# if __name__ == "__main__":
#   asyncio.run(create_admin())
