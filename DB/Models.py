import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()
class Users_info(Base):
    __tablename__ = "users_info"
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.VARCHAR(length=40), nullable=False)
    second_name = sq.Column(sq.VARCHAR(length=40), nullable=False)
    age = sq.Column(sq.Integer)
    city = sq.Column(sq.VARCHAR(length=40))
    sex = sq.Column(sq.Integer)
    def __str__(self):
        return f'Users_info {self.id}: ({self.first_name}, {self.second_name}, {self.city}, {self.age}, {self.sex})'

class White_list(Base):
    __tablename__ = "white_list"
    id_user = sq.Column(sq.Integer, primary_key=True)
    id_db_user = sq.Column(sq.Integer, sq.ForeignKey(Users_info.id))

    users_info = relationship(Users_info, cascade="all,delete", backref="white_list")
    def __str__(self):
        return f'White_list {self.id_user}: {self.id_db_user}'

class Black_list(Base):
    __tablename__ = "black_list"
    id_user = sq.Column(sq.Integer, primary_key=True)
    id_db_user = sq.Column(sq.Integer, sq.ForeignKey(Users_info.id))

    users_info = relationship(Users_info, cascade="all,delete", backref="black_list")
    def __str__(self):
        return f'Black_list {self.id_user}: {self.id_db_user}'



def create_table(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
