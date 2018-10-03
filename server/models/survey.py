import sqlite3

## internal representation

class SurveyModel:
    def __init__(self):
        pass

    # returns a json representation of the model
    def json(self):
        pass


    #find a survey by its name, should be classmethod, because it returns an object of Survey Model
    @classmethod
    def find_by_name(cls, name):
        pass
