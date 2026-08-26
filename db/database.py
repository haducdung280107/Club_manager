from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DATABASE_URL="mysql+pymysql://root:123456789@localhost:3306/demo_club"

engine=create_engine(SQL_DATABASE_URL)

Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()