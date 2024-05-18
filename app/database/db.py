from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql://sail:password@mysql:3306/ocr_api_db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# class MySQL:
#     DATABASE_URL = "mysql://sail:password@mysql:3306/ocr_api_db"
#     engine = None
#     session_local = None
#     base = None
#
#     def __init__(self):
#         self.engine = create_engine(self.DATABASE_URL, connect_args={"check_same_thread": False})
#         self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
#         self.base = declarative_base()
