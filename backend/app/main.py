from fastapi import FastAPI
from .db import init_db
from .routes import router as api_router

app = FastAPI(title="Social Grow Starter")
@app.on_event("startup")
def startup():
    init_db()

app.include_router(api_router, prefix="/api")
