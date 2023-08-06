from db.models import (User, List, Task, Menu)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from rich.table import Table


class app:

    def __init__(self):
        
        self.selected_user = None
        self.selected_list = None
        self.selected_task = None
        self.main_menu = Menu({1: self.make_user, 2: self.fetch_user, 3: self.delete_user})
        self.user_menu = Menu({1: self.select_list, 2: self.make_list, 3: self.delete_list})
        self.list_menu = Menu({1: self.make_task, 2: self.delete_task, 3: self.select_task})
        self.task_menu = Menu({1: self.change_status, 2: self.change_task_description})

    def run_app(self):

        self.main_menu.loop()

    def make_user(self):

        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")

        new_user = User(first_name = f_name, last_name = l_name)
        session.add(new_user)
        session.commit()
        self.selected_user = new_user
        if self.selected_user:
            self.user_menu.loop()
    
    def fetch_user(self):

        console = Console()
        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")
        self.selected_user = session.query(User).filter(User.first_name == f_name and User.last_name == l_name).first()
        if (self.selected_user):
            console.print(self.selected_user.__repr__())
            self.user_menu.loop()
        else:
            print("User not found.")

    def delete_user(self):
        
        f_name = input("Enter user name to be deleted: ")
        user_id = int(input("Enter user id to be deleted: "))
        
        if f_name and user_id and type(user_id) == int:
            delete_user = session.query(User).filter(User.id == user_id and User.first_name == f_name).first()
            session.delete(delete_user)
            session.commit()

        else: 
            print("Invalid name or id.")


    def select_list(self):

        user_console = Console()
        user_console.print(self.selected_user.__repr__())

        list_name = input("Select List: ")
        self.selected_list = session.query(List).filter(List.name == list_name).first()

        if self.selected_list:
            list_console = Console()
            list_console.print(self.selected_list.__repr__())
            self.list_menu.loop()
        else:
            print("List not found")

    def make_list(self):
        
        list_name = input("Enter List name: ")
        new_list = List(name = list_name, user_id = self.selected_user.id)
        session.add(new_list)
        session.commit()
        
    def delete_list(self):

        console = Console()
        console.print(self.selected_user.__repr__())
        list_name = input("Enter list to be deleted: ")
        list_id = int(input("Enter list id: "))
        delete_list = session.query(List).filter(List.name == list_name and List.id == list_id).first()
        session.delete(delete_list)
        session.commit()


    def make_task(self):

        task_description = input("Enter task: ")

        if task_description:
            new_task = Task(description = task_description, list_id = self.selected_list.id)
            session.add(new_task)
            session.commit()

        else:
            print("Task description must be non-empty string!")
        
        console = Console()
        console.print(self.selected_list.__repr__())


    def delete_task(self):

        console = Console()
        console.print(self.selected_list.__repr__())

        task_id = input("Enter task id to be deleted: ")

        if task_id:
            delete_task = session.query(Task).filter(Task.id == task_id).first()
            session.delete(delete_task)
            session.commit()

    def select_task(self):

        console = Console()
        console.print(self.selected_list.__repr__())

        task_description = input("Select Task: ")
        self.selected_task = session.query(Task).filter(Task.description == task_description).first()
        if self.selected_task:
            self.task_menu.loop()
        else:
            print("Task not found")

    def change_status(self):
        pass

    def change_task_description(self):
        pass




if __name__ == '__main__':

    engine = create_engine('sqlite:///todo.db')
    Session = sessionmaker(bind=engine)
    session = Session()
        
    app().run_app()
    


