import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="probleme mit dem usernamen"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="probleme mit dem passwort"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data) # UserModel(**data)
        #user = UserModel(data['username'],data['password']) # UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO USERS VALUES (NULL, ?, ?)" # NULL fuer auto increment
        # cursor.execute(query,(data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()
