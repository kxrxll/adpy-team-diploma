import sqlalchemy
import configparser
from sqlalchemy.orm import sessionmaker
from Models import create_table

config = configparser.ConfigParser()
config.read("settings.ini")
engine = sqlalchemy.create_engine(config["DSN"]["DSN"])
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.close()
