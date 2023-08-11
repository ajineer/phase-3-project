This Python project consists of a set of classes that model a basic task management system using SQLAlchemy. The project is structured to create and manage users, lists, tasks, and categories, providing functionality for creating, updating, and organizing tasks within lists.

Prerequisites
Before using this project, ensure you have the following installed:

Python (3.x recommended)
SQLAlchemy
Rich Library
Project Structure
The project is organized into several classes, each serving a specific role within the task management system:

User: Represents a user with a first name, last name, and associated lists.
List: Represents a list of tasks owned by a user.
Task: Represents a task within a list, including its description and completion status.
Category: Represents a category that tasks can be associated with.
Menu: Implements a simple menu system for user interaction.
How to Use
Import Required Libraries

Make sure you have imported the necessary libraries at the beginning of your script:

python
Copy code
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Table
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from rich.table import Table as TB
Create Classes

Copy the class definitions from the provided code into your project file.

Database Setup

Set up your database using SQLAlchemy's database creation and configuration methods. You need to import Base from the project and use it as a base class for your declarative models.

python
Copy code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///your_database.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
Using the Classes

You can now utilize the defined classes to create, update, and manage tasks and lists within your application. Here's an example of how you might interact with the classes:

python
Copy code
session = Session()

# Creating a user

user = User(first_name="John", last_name="Doe")
session.add(user)
session.commit()

# Creating a list and tasks

task_list = List(name="My Tasks", user=user)
task1 = Task(description="Complete project", list=task_list)
task2 = Task(description="Buy groceries", list=task_list)
session.add(task_list)
session.commit()

# Associating tasks with categories

category1 = Category(title="Work")
category2 = Category(title="Personal")
task1.categories.append(category1)
task2.categories.append(category2)
session.commit()

# Displaying user's lists and tasks

print(user)
print(task_list)

session.close()
Running the Menu System
The provided Menu class can be used to interact with your project's functionality in a user-friendly manner. To use the menu, create instances of your classes and provide them to the Menu as options. Here's an example of how to use the menu:

python
Copy code

# Create instances of classes

user = User(first_name="John", last_name="Doe")
task_list = List(name="My Tasks", user=user)

# Create a dictionary of menu options

menu_options = {
1: user,
2: task_list, # Add more options as needed
}

# Create a menu instance and start the loop

menu = Menu(menu_options)
menu.loop()
Conclusion
This project provides a basic foundation for managing tasks within lists and associating them with categories using SQLAlchemy. Feel free to extend and customize the functionality to suit your specific needs and build upon this project's capabilities. If you have any questions or encounter issues, don't hesitate to refer to SQLAlchemy's documentation or seek assistance from the community.

### What Goes into a README?

This README should serve as a template for your own- go through the important
files in your project and describe what they do. Each file that you edit
(you can ignore your Alembic files) should get at least a paragraph. Each
function should get a small blurb.

You should descibe your actual CLI script first, and with a good level of
detail. The rest should be ordered by importance to the user. (Probably
functions next, then models.)

Screenshots and links to resources that you used throughout are also useful to
users and collaborators, but a little more syntactically complicated. Only add
these in if you're feeling comfortable with Markdown.

---

## Conclusion

A lot of work goes into a good CLI, but it all relies on concepts that you've
practiced quite a bit by now. Hopefully this template and guide will get you
off to a good start with your Phase 3 Project.

Happy coding!

---

## Resources

- [Setting up a respository - Atlassian](https://www.atlassian.com/git/tutorials/setting-up-a-repository)
- [Create a repo- GitHub Docs](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
