from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# from psycopg.rows import dict_row
# import psycopg
# from time import sleep

# while True:
#     try:
#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastapi",
#             port=6491,
#             user="postgres",
#             password="P-Qlolik123",
#             row_factory=dict_row,
#         )
#         print("DB connection was successful")
#         break
#     except Exception as e:
#         print(f"Connecting failed\nERROR: {e}")
#         sleep(5)