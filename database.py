from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:buymecoffeefirst80ko@localhost:5432/telusco"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)