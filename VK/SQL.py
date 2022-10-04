import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DSN
from Models import create_table, Users_info, Black_list, White_list

engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()