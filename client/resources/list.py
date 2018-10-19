from flask_restful import Resource, reqparse

from models.clientlist import ListModel
import json



class Liste(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="name is missing"
    )
    parser.add_argument('liste',
        type=str,
        action='append',
        required=True,
        help="liste is missing"
    )
    parser.add_argument('antworten',
        type=int,
        action='append',
        required=True,
        help="antworten is missing"
    )

    def get(self,name):
        test = ListModel.find_by_name(name)
        if test:
            #return survey.json()
            return test.json()
        return {'message': "Listentest with name '{}' not found".format(name)}, 404 #not found

    def post(self,name):
        #if AnswerModel.find_by_name(aname):
            #schreibe zeugs in db
        data = Liste.parser.parse_args()
        test = ListModel(name,
        json.dumps(data['liste']),json.dumps(data['antworten']))
        #try:
        test.save_to_db()
        #except:
        #    return {'message': "error while inserting question with qname '{}'. ".format(qname)}, 500
        return test.json(), 201 # status created



# Testing Resource: returns a list with all reports in the database
class ListAll(Resource):
    def get(self):
        return {'tests': [ x.json() for x in ListModel.query.all()]}
