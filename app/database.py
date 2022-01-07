from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://vivek:password#123@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2
# from psycopg2.extras import RealDictCursor

# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="vivek",
#         password="password#123",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Database connection successesfull!")
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error: ", error)
#     exit()
