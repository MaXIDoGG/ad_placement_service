from fastapi import Depends, FastAPI, HTTPException, status
import logging
import uvicorn
from auth import router as auth_router
# from users import router as users_router

app = FastAPI()

logging.getLogger('passlib').setLevel(logging.ERROR)


app.include_router(router=auth_router.router)
# app.include_router(router=users_router.router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
