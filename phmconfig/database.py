from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import constants

#  "sqlite:///./app.db"
#   "mysql+pymysql://root:123465@192.168.101.59:3306/phmmysql"
#   "postgresql+psycopg2://postgres:postgres@192.168.101.59:5432/phmmsdb"

engine = create_engine(
    constants.PHM_DATABASE_URL #,
   # connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


def create_tables() -> list:
    Base.metadata.create_all(bind=engine)
    return list(Base.metadata.tables.keys())
