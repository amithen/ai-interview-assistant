from sqlalchemy import Column, Integer, ForeignKey,Text,DateTime
from datetime import datetime

from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    filename = Column(Text, nullable=False)

    raw_text = Column(Text, nullable=False)

    ai_response = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)