from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import (relationship, mapped_column)

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer(), primary_key = True)
    lists = relationship(
        "List", 
        back_populates = "users",
        cascade="all, delete, delete-orphan",
    )
    first_name = Column(String())
    last_name = Column(String())

    def __repr__(self):
        return f"{self.id}: " \
        + f" First Name: {self.first_name}" \
    
class List(Base):
    
    __tablename__ = "lists"

    id = Column(Integer(), primary_key = True)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"))
    users = relationship("User", back_populates="lists")
    tasks = relationship(
        "Task",
        back_populates = "lists",
        cascade = "all, delete, delete-orphan",
    )
    name = Column(String())

    def __repr__(self):
        return f"{self.id}: " \
        +f" Name: {self.name}" \
        +f" User id: {self.user_id}"
    
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer(), primary_key = True)
    list_id = Column(Integer(), ForeignKey("lists.id", ondelete="CASCADE"))
    lists = relationship("List", back_populates="tasks")
    description = Column(String())

    def __repr__(self):
        return f"{self.id}: " \
        +f" Description: {self.description}" 

