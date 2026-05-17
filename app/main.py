from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import engine


app = FastAPI()
@app.get("/")
async def home():
    return {"message": "AI Interview Assistant API Running"}

@app.get("/health")
async def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "healthy"}

