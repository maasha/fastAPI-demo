from sqlalchemy import Column, Integer, String
from app.database import Base


class UserDB(Base):
    """SQLAlchemy User model for database"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(200), nullable=False)

