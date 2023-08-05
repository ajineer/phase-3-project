from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///todo.db')
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key = True)
    first_name = Column(String())
    last_name = Column(String())
    lists = relationship("List", backref=backref('user'), cascade = 'all, delete-orphan')
    

    def __repr__(self):
        return f"User: {self.id} " \
        + f"First Name: {self.first_name}" \
    
class List(Base):
    
    __tablename__ = 'lists'

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    user_id = Column(String(), ForeignKey('users.id'))
    tasks = relationship("Task", backref=backref('list'), cascade = 'all, delete-orphan')

    def __repr__(self):
        return f"List id: {self.id}" \
        +f"Name: {self.name}" \
        +f"User id: {self.user_id}"
    
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer(), primary_key = True)
    description = Column(String())
    list_id = Column(String(), ForeignKey('lists.id'))
    user_id = Column(String(), ForeignKey('users.id'))

    def __repr__(self):
        return f"Task id: {self.id}" \
        +f"{self.description}" 

