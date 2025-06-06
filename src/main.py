from fastapi import Depends, FastAPI, HTTPException, status
import logging
from auth import router

app = FastAPI()

logging.getLogger('passlib').setLevel(logging.ERROR)


app.include_router(router=router.router)