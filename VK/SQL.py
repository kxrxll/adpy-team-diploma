import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DSN
from Models import create_table, Users_info, Black_list, White_list
import VK

engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

for c in session.query(Users_info).filter(Users_info.sex ==2, Users_info.city =='Санкт-Петербург', Users_info.age >=33, Users_info.age <= 34, ).all():
    print(c)

session.close()