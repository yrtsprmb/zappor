import sqlite3
from flask_restful import Resource
from models.user import UserModel

import resources.parsers

class UserRegister(Resource):

    def post(self):
        data = resources.parsers.ParseUser.parser.parse_args()

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
