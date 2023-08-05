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
    email = Column(String(55))
    lists = relationship("List", backref=backref('user'))
    

    def __repr__(self):
        return f"User: {self.id} " \
        + f" {self.first_name}" \
        + f" {self.last_name}" \
        + f" {self.email}"
    
class List(Base):
    
    __tablename__ = 'lists'

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    user_id = Column(String(), ForeignKey('users.id'))
    tasks = relationship("Task", backref=backref('list'))

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
        +f"{self.description}" \
        +f"{self.list_id}" \
        +f"{self.user_id}"


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

