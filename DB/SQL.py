import sqlalchemy
import configparser
from sqlalchemy.orm import sessionmaker
from Models import create_table, Users_info, Black_list, White_list
import VK

config = configparser.ConfigParser()
config.read("settings.ini")
engine = sqlalchemy.create_engine(config["DSN"]["DSN"])
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()
for c in session.query(Users_info).filter(Users_info.sex == 2, Users_info.city == 'Санкт-Петербург',
                                          Users_info.age >= 33, Users_info.age <= 34, ).all():
    print(c)
session.close()
