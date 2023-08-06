from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer(), primary_key = True)
    lists = relationship(
        "List", 
        back_populates = "users",
        cascade="all, delete, delete-orphan",
    )
    _first_name = mapped_column("first name", String())
    _last_name = mapped_column("last name", String())

    @hybrid_property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, first_name):
        
        if isinstance(first_name, str) and first_name and len(first_name) > 0:
            self._first_name = first_name
        else:
            print("Invalid first name")
            raise ValueError
        
    @hybrid_property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and last_name and len(last_name) > 0:
            self._last_name = last_name
        else:
            print("Invalid last name")
            raise ValueError

    def __repr__(self):
        return f"{self.id}: " \
        + f" First Name: {self.first_name}" \
    
class List(Base):
    
    __tablename__ = "lists"

    id = Column(Integer(), primary_key = True)
    user_id = mapped_column("user id", Integer(), ForeignKey("users.id", ondelete="CASCADE"))
    users = relationship("User", back_populates="lists")
    tasks = relationship(
        "Task",
        back_populates = "lists",
        cascade = "all, delete, delete-orphan",
    )
    _name = mapped_column("name", String())

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and name and not hasattr(self, name):
            self._name = name
        else:
            raise ValueError("List name must be non-empty string!")

    def __repr__(self):
        return f"{self.id}: " \
        +f" Name: {self.name}" \
        +f" User id: {self.user_id}"
    
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer(), primary_key = True)
    list_id = mapped_column("list id", Integer(), ForeignKey("lists.id", ondelete="CASCADE"))
    lists = relationship("List", back_populates="tasks")
    _description = mapped_column("description", String())
    _complete = mapped_column("completed", Integer(), default=0)

    @hybrid_property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if description and isinstance(description, str):
            self._description = description

    def __repr__(self):
        return f"{self.id}: " \
        +f" Description: {self.description}" 

