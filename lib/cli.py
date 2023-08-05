from db.models import (User, List, Task)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

class app:

    def __init__(self):
        
        self.selected_user = None
        self.selected_list = None
        self.selected_task = None
        self.main_menu = Menu({1: self.make_user, 2: self.fetch_user, 3: self.delete_user})
        self.user_menu = Menu({1: self.select_list, 2: self.make_list})
        self.list_menu = Menu({1: self.make_task})

    def run_app(self):

        self.main_menu.loop()

    def make_user(self):

        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")

        if f_name and len(f_name) >= 1 and l_name and len(l_name) >= 1:
            new_user = User(first_name = f_name, last_name = l_name)
            session.add(new_user)
            session.commit()
        else:
            print("first and last name must be non-empty strings!")
    
    def fetch_user(self):

        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")
        self.selected_user = session.query(User).filter(User.first_name == f_name and User.last_name == l_name).first()
        if (self.selected_user):
            user_lists = session.query(List).filter(List.user_id == self.selected_user.id)
            if user_lists:
                print([li for li in user_lists])
            else:
                print("User has no lists.")
            self.user_menu.loop()
        else:
            print("User not found.")

    def delete_user(self):
        
        f_name = input("Enter user name to be deleted: ")
        user_id = int(input("Enter user id to be deleted: "))
        
        if f_name and user_id and type(user_id) == int:
            delete_user = session.query(User).filter(User.id == user_id and User.first_name == f_name)
            session.delete(delete_user)
            session.commit()

        else: 
            print("Invalid name or id.")


    def select_list(self):

        list_name = input("Select List: ")
        self.selected_list = session.query(List).filter(List.name == list_name).first()

        if self.selected_list:
            print(self.selected_list)
            tasks = session.query(Task).filter(Task.list_id == self.selected_list.id).all()
            if tasks:
                print([task for task in tasks])
            else:
                print("No tasks in this list")
            self.list_menu.loop()
        else:
            print("List not found")

    def make_list(self):
        
        list_name = input("Enter List name: ")
        new_list = List(name = list_name, user_id = self.selected_user.id)
        session.add(new_list)
        session.commit()

    def make_task(self):

        task_description = input("Enter task: ")

        if task_description:
            new_task = Task(description = task_description, list_id = self.selected_list.id, user_id = self.selected_user.id)
            session.add(new_task)
            session.commit()

        else:
            print("Task description must be non-empty string!")




if __name__ == '__main__':

    engine = create_engine('sqlite:///todo.db')
    Session = sessionmaker(bind=engine)
    session = Session()
        
    app().run_app()
    


