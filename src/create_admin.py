from models import async_session, User
from auth.utils import get_password_hash
import asyncio
session = async_session()

async def create_admin():
	admin = User(
		login="admin",
		name="admin",
		password_hash = get_password_hash("admin"),
		is_admin = True
	)
	session.add(admin)
	await session.commit()
 
if __name__ == "__main__":
  asyncio.run(create_admin())
