from sqlalchemy import Boolean, Column, String
from app.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
