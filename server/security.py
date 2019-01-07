#security.py
from werkzeug.security import safe_str_cmp
from models.users import UserModel

'''
If user exists and password is correct user will be authenticated.
'''
def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
