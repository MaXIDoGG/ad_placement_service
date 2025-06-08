from fastapi import FastAPI
import asyncio
from auth import router as auth_router
from ads import router as ads_router
from users import router as users_router
from database import init_models, create_admin

app = FastAPI()
asyncio.create_task(init_models())
asyncio.create_task(create_admin())

app.include_router(router=auth_router.router)
app.include_router(router=ads_router.router)
app.include_router(router=users_router.router)


# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
