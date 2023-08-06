from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from rich.table import Table

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
         
        user_table = Table(title = self.first_name)
        user_table.add_column("Lists")
        user_table.add_column("id")

        if self.lists:
            for list in self.lists:
                user_table.add_row(list.name, f"{list.id}")
        else:
            user_table.add_row("no lists")
        
        return user_table
    
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
        
        list_table = Table(title = self.name)
        list_table.add_column("id")
        list_table.add_column("Task")
        list_table.add_column("Status")
        if self.tasks:
            for task in self.tasks:
                list_table.add_row(f"{task.id}", task.description, "Complete" if task.complete == 1 else "Incomplete")
        else:
            list_table.add_row("n/a", "no tasks")
        return list_table
    
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer(), primary_key = True)
    list_id = mapped_column("list id", Integer(), ForeignKey("lists.id", ondelete="CASCADE"))
    lists = relationship("List", back_populates="tasks")
    _description = mapped_column("description", String())
    complete = mapped_column("completed", Integer(), default=0)

    @hybrid_property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if description and isinstance(description, str):
            self._description = description

    def __repr__(self):
        return f"{self.id}: " \
        +f" Description: {self.description}" \
        +f" Status: {'complete' if self.complete == 1 else 'incomplete'}" 

class Menu:

    def __init__(self, dictionary):

        self.dictionary = dictionary
        self.choice = 0
        self.endBound = int(len(self.dictionary)) + 1

    def display(self, index=1):
        if(index == 1):
            print(f"\033[33m{'='*6*len(self.dictionary)}\033[0m")
        print(f"\033[33m{index}:\033[0m {self.dictionary[index].__name__}")
        if(index == len(self.dictionary)):
            print(f"\033[33m{self.endBound}:\033[0m Exit")
            print(f"\033[33m{'='*6*len(self.dictionary)}\033[0m")
            pass
        else:
            return self.display(index+1) 
        
    def loop(self):
        self.display()
        try:
            print(f"\033[34m<{'-'*5*len(self.dictionary)}>\033[0m")
            choice = int(input("Enter choice: "))
            print(f"\033[34m<{'-'*5*len(self.dictionary)}>\033[0m")
            if(choice < 1 or choice > self.endBound):
                print("Choice out of range try again")
                return self.loop()
            else:
                if(choice == self.endBound):
                    pass
                else:
                    print(f"\033[32m<{'-'*5*len(self.dictionary)}>\033[0m")
                    self.dictionary[choice]()
                    print(f"\033[32m<{'-'*5*len(self.dictionary)}>\033[0m")
                    return self.loop()
        except ValueError:
            print("You did not enter an integer value.")
            return self.loop()