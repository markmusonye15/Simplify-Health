from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from db.config import DATABASE_URL
from db.database import db
from controllers import users_controller
import bcrypt

# initialize out application instance
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

db.init_app(app)

migrate = Migrate(app, db)

# JWT Initialization
jwt = JWTManager(app)

from models.user import User, UserType


@app.route("/login", methods=["POST"])
def login():
    login_credentials = request.get_json()

    username = login_credentials['username']
    password = login_credentials['password']
    print('Received data:', username, password)

    # check if the user exists
    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify({'message': f'User with username {username} does not exist'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    return jsonify({"message": "Username or password is invalid"}), 401


@app.route("/users/register", methods=["POST"])
def register():

    if request.method == "POST":
        user_details = request.get_json()

        username = user_details['username']
        email = user_details["email"]
        password = user_details['password']

        # hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt=bcrypt.gensalt())

        user = UserType(
            id=None,
            username=username,
            email=email,
            password=hashed_password.decode('utf-8')
        )

        users_controller.create_a_new_user(user)

        return jsonify({"message": "User registered successfully"}), 201


# declare a route
@app.route('/')
@jwt_required()
def welcome():
    return jsonify({"message": "WELCOME TO MY HEALTH E APPLICATION", "success": "ok"})


@app.route('/users')
@jwt_required()
def fetch_all_users():
    """
    List all users
    """
    # convert the my_users to json
    my_users = users_controller.get_all_users()

    users_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
            # avoid including password in API response!
        }
        for user in my_users
    ]

    return jsonify(users_list)


@app.route('/user/<int:id>')
@jwt_required()
def fetch_user(id):
    # filter the list and get the user that matched the id
    user = users_controller.get_a_single_user(id)

    if user:
        return jsonify(user)
    return jsonify({"message": "User Not Found"})


@app.route('/user/update/<int:id>')
@jwt_required()
def update_user(id):
    # filter the list and get the user that matched the id

    user_obj = {
        "username": "John Doe Example",
        "email": "johndoe@gmail.com"
    }

    user = users_controller.get_a_users_and_update(id, user_obj)

    return jsonify(user)


@app.route('/user/delete/<int:id>')
@jwt_required()
def delete_user(id):
    # filter the list and get the user that matched the id
    users_controller.get_a_user_and_delete(id)
    return jsonify({"message": "User Deleted"})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
