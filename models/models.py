from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
from datetime import datetime

db = create_engine("sqlite:///./database/database.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    email = Column('email', String, nullable=False)
    password = Column('password', String)
    active = Column('active', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String)
    user = Column('user', ForeignKey('users.id'))
    amount = Column('price', Float)
    type_flow = Column('type_flow', String)
    category = Column('category', String)
    #created_at = Column('created_at', default=datetime.utcnow)

    def __init__(self, user, type_flow, category, amount=0):
        self.user = user
        self.type_flow = type_flow
        self.category = category
        self.amount = amount



