#!/usr/bin/env python3

from models import (User, List, Task, Category)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rich.console import Console
from rich.table import Table as TB
import inquirer


class Menu:

    all = []
    currentIndex = 0

    def __init__(self, menu_dict):

        self.menu_dict = menu_dict
        self.questions = [
            inquirer.List("functions", message="Select an option", choices = self.menu_dict.keys())
        ]
        
        Menu.all.append(self)

    def loop(self):
        Menu.currentIndex = Menu.all.index(self)
        answers = inquirer.prompt(self.questions)
        self.menu_dict.get(answers['functions'])()
        
class app:

    def __init__(self):
        
        self.selected_user = None
        self.selected_list = None
        self.selected_task = None
        self.selected_category = None

    def create_menus(self):

        self.main_menu = Menu({
            self.make_user.__name__: self.make_user, 
            self.fetch_user.__name__: self.fetch_user, 
            self.delete_user.__name__: self.delete_user, 
            self.exit.__name__: self.exit})
        
        self.user_menu = Menu(
            {self.select_list.__name__: self.select_list, 
             self.make_list.__name__: self.make_list, 
             self.delete_list.__name__:self.delete_list, 
             self.make_category.__name__:self.make_category, 
             self.back.__name__: self.back})
        
        self.list_menu = Menu({
            self.select_task.__name__: self.select_task, 
            self.make_task.__name__: self.make_task, 
            self.delete_task.__name__: self.delete_task, 
            self.show_by_category.__name__: self.show_by_category,
            self.back.__name__: self.back})
        
        self.task_menu = Menu({
            self.change_status.__name__: self.change_status, 
            self.change_task_description.__name__: self.change_task_description, 
            self.back.__name__: self.back})
    
    def save_to_db(self, save_object):
        session.add(save_object)
        session.commit()

    def delete_from_db(self, delete_obj):
        session.delete(delete_obj)
        session.commit()

    def run_app(self):

        self.main_menu.loop()

    def back(self):

        return_functions = {
            1: self.main_loop,
            2: self.user_loop,
            3: self.list_loop,
            4: self.task_loop
            }
    
        return_functions.get(Menu.currentIndex)()
        
    def print_console(self, table):
        
        console = Console()
        console.print(table)

    def exit(self):

        return 1
    
    def main_loop(self):

        self.main_menu.loop()

    def user_loop(self):

        self.print_console(self.selected_user.__repr__())
        self.user_menu.loop()

    def list_loop(self):
        
        self.print_console(self.selected_list.__repr__())
        self.list_menu.loop()

    def task_loop(self):

        self.print_console(self.selected_task.__repr__())
        self.task_menu.loop()

    def fetch_user(self):

        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")
        self.selected_user = session.query(User).filter(User.first_name == f_name and User.last_name == l_name).first()

        if (self.selected_user):
            
            self.user_loop()
        
        else:

            print("User not found.")
            self.main_menu.loop()
    
    def select_list(self):

        self.print_console(self.selected_user.__repr__())
        list_name = input("Select List: ")
        self.selected_list = session.query(List).filter(List.name == list_name).first()

        if self.selected_list:
            
            self.list_loop()
        
        else:

            print("List not found")
            self.user_menu.loop()

    def select_task(self):

        self.print_console(self.selected_list.__repr__())

        task_description = input("Select Task: ")
        self.selected_task = session.query(Task).filter(Task.description == task_description).first()
        
        if self.selected_task:

            self.task_loop()
        
        else:

            print("Task not found")
            self.list_loop()

    def make_user(self):

        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")

        new_user = User(first_name = f_name, last_name = l_name)
        self.save_to_db(new_user)
        self.selected_user = new_user

        if self.selected_user:
            self.user_loop()
    
    def make_list(self):
        
        list_name = input("Enter List name: ")
        new_list = List(name = list_name, user_id = self.selected_user.id)

        if new_list:

            self.save_to_db(new_list)
            self.selected_list = new_list
            self.list_loop()

    def make_category(self):
        
        new_title = input("Enter input: ")

        if new_title:
            
            new_cat = Category(title=new_title)
            self.save_to_db(new_cat)

        else:

            print("Category can't be empty!")
        
        self.list_loop()


    def make_task(self):

        task_description = input("Enter task: ")

        if task_description:

            new_task = Task(description = task_description, list_id = self.selected_list.id)
            categories = session.query(Category).all()
        
            cat_list = [inquirer.Checkbox("Categories", message="Select Category", choices = [cat.title for cat in categories])]
            answers = inquirer.prompt(cat_list)
            self.selected_category = answers["Categories"]
            new_task.categories = session.query(Category).filter(Category.title.in_(answers["Categories"])).all()
            self.save_to_db(new_task)

        else:

            print("Task description must be non-empty string!")
        
        self.list_loop()

    def delete_user(self):
        
        f_name = input("Enter user name to be deleted: ")
        user_id = int(input("Enter user id to be deleted: "))
        
        if f_name and user_id and type(user_id) == int:

            delete_user = session.query(User).filter(User.id == user_id and User.first_name == f_name).first()
            self.delete_from_db(delete_user)

        else: 

            print("Invalid name or id.")
        
        self.main_loop()

    def delete_list(self):

        self.print_console(self.selected_user.__repr__())
        list_name = input("Enter list to be deleted: ")
        list_id = int(input("Enter list id: "))
        delete_list = session.query(List).filter(List.name == list_name and List.id == list_id).first()
        self.delete_from_db(delete_list)
        self.user_loop()

    def delete_task(self):

        self.print_console(self.selected_list.__repr__())

        task_id = int(input("Enter task id to be deleted: "))

        if task_id:
            delete_task = session.query(Task).filter(Task.id == task_id).first()
            self.delete_from_db(delete_task)

        else:
            print("Invalid task description!")

        self.list_loop()

    def change_status(self):
        
        change_options = [inquirer.List("choices", message="Select incomplete or complete", choices=["Incomplete", "Complete"])]
        answer = inquirer.prompt(change_options)
        fetch_task = session.query(Task).filter(Task.id == self.selected_task.id).first()
        fetch_task.complete = 0 if answer["choices"] == "Incomplete" else 1
        session.commit() 
        self.task_loop()

    def change_task_description(self):
        
        self.print_console(self.selected_task.__repr__())
        new_description = input("Enter new description: ")
        fetch_task = session.query(Task).filter(Task.id == self.selected_task.id).first()
        fetch_task.description = new_description
        session.commit()
        self.selected_task = session.query(Task).filter(Task.id == self.selected_task.id).first()
        self.task_loop()

    def show_by_category(self):
        
        choices = [inquirer.List("choices", message="Select a Category", choices=[cat.title for cat in session.query(Category).all()])]
        answer = inquirer.prompt(choices)
        tasks = session.query(Task).filter(Task.list_id == self.selected_list.id and Task.categories.in_(answer["choices"]))
        task_table = TB(title = "Task by Category")
        task_table.add_column("id")
        task_table.add_column("Category")
        task_table.add_column("Task")
        
        for task in tasks:
            task_table.add_row(f"{task.id}", answer["choices"], task.description)
        self.print_console(task_table)
        self.task_loop()

if __name__ == '__main__':

    engine = create_engine('sqlite:///todo.db')
    Session = sessionmaker(bind=engine)
    session = Session()
        
    my_app = app()
    my_app.create_menus()
    my_app.run_app()
    


