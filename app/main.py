from fastapi import FastAPI
from app.controllers import api_router

app = FastAPI(title="Home API")
app.include_router(api_router)
