from flask import Flask
import json

# initialize out application instance
app = Flask(__name__)

my_users = [
    {
        "id": 1,
        "name": "John Kamau",
        "hobbies": ["Driving", "Swimming", "Listening to Music"]
    },
    {
        "id": 2,
        "name": "Silvester Mburu",
        "hobbies": ["Boxing", "Meditating", "Sleeping"]
    },
    {
        "id": 3,
        "name": "Lynn Kolii",
        "hobbies": ["Reading Novels", "Shopping", "Socializing"]
    }
]


# declare a route
@app.route('/')
def welcome():
    return "<p>WELCOME TO MY HEALTH E APPLICATION </p>"


@app.route('/users')
def fetch_all_users():
    """
    List all users
    """
    # convert the my_users to json
    return json.dumps(my_users)


@app.route('/user/<int:id>')
def fetch_user(id):
    # filter the list and get the user that matched the id
    for user in my_users:
        if user["id"] == id:
            return json.dumps(user)
    return {"message": "User Not Found"}


@app.route('/user/update/<int:id>')
def update_user(id):
    # filter the list and get the user that matched the id
    for user in my_users:
        if user["id"] == id:
            # UPDATE THE INFORMATION IN THE LIST
            user["name"] = "John Doe Example"
            return json.dumps(user)
    return {"message": "User Not Found"}


@app.route('/user/delete/<int:id>')
def delete_user(id):

    # filter the list and get the user that matched the id
    for user in my_users:
        if user["id"] == id:

            # I do have the user object id, name, hobbies
            my_users.remove(user)

            return {"message": "User Deleted"}
    return {"message": "User Not Found"}



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
