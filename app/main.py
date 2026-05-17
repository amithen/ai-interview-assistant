from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import engine,Base
from app.api.auth import router as auth_router
from app.models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine) #creates tables,Creates all tables automatically.
app.include_router(auth_router)
@app.get("/")
def home():
    return {"message": "AI Interview Assistant API Running"}


@app.get("/health")
def health_check():

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "Database Connected"}


