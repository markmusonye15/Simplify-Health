from models.user import User, UserType
from db.database import db


def get_all_users():
    users = db.session.query(User).all()
    print("USERS", users)
    return users


def get_a_single_user(id: int):
    user = db.session.query(User).filter_by(User.id == id).first()
    if user is None:
        print(f"User with ID {id} does not exist")
    print("USER", user)
    return user


def create_a_new_user(user: UserType):
    user_details = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    new_user = User.create(user_details)
    print("USER", new_user)
    return new_user


def get_a_users_and_update(id: int, userObj):

    user = db.session.query(User).filter_by(User.id == id).first()

    if user is None:
        print(f"User with ID {id} does not exist")

    user["username"] = userObj["username"]
    user["email"] = userObj['email']

    new_user_info = User.update(user)
    print("User", new_user_info)
    return new_user_info


def get_a_user_and_delete(id: int):

    user = db.session.query(User).filter_by(User.id == id)

    if user is None:
        print(f"User with ID {id} does not exist")

    User.delete(user)
    print(f"User with ID {id} has been deleted successfully")
    return True
