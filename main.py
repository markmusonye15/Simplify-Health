from flask import Flask, jsonify
from flask_migrate import Migrate
from db.config import DATABASE_URL
from db.database import db
from controllers import users_controller

# initialize out application instance
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)

migrate = Migrate(app, db)

from models.user import User


# declare a route
@app.route('/')
def welcome():
    return jsonify({"message": "WELCOME TO MY HEALTH E APPLICATION", "success": "ok"})


@app.route('/users')
def fetch_all_users():
    """
    List all users
    """
    # convert the my_users to json
    my_users = users_controller.get_all_users()
    return jsonify(my_users)


@app.route('/user/<int:id>')
def fetch_user(id):
    # filter the list and get the user that matched the id
    user = users_controller.get_a_single_user(id)

    if user:
        return jsonify(user)
    return jsonify({"message": "User Not Found"})


@app.route('/user/update/<int:id>')
def update_user(id):
    # filter the list and get the user that matched the id

    user_obj = {
        "username": "John Doe Example",
        "email":"johndoe@gmail.com"
    }

    user = users_controller.get_a_users_and_update(id, user_obj)

    return jsonify(user)


@app.route('/user/delete/<int:id>')
def delete_user(id):
    # filter the list and get the user that matched the id
    users_controller.get_a_user_and_delete(id)
    return jsonify({"message": "User Deleted"})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
