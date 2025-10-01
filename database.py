from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use SQLite for development, PostgreSQL for production
if os.getenv("ENVIRONMENT") == "production":
    DATABASE_URL = "postgresql://mypguser:newpassword@db:5432/mypgdb"
else:
    DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
