from models import User, Category, Task, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":

    engine = create_engine('sqlite:///todo.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    c1 = Category(_title = "Personal")
    c2 = Category(title = "Chores")
    c3 = Category(title = "Errands")

    session.bulk_save_objects([c1,c2,c3])
    session.commit()
    