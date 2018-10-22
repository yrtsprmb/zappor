import json
from flask_restful import Resource, reqparse

from models.answers import AnswerModel

#REST API for Answers
class Answer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="name is missing"
    )
    parser.add_argument('type',
        type=str,
        required=True,
        help="liste is missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=True,
        help="options are missing"
    )
    parser.add_argument('answer',
        type=str,
        action='append',
        required=True,
        help="answer is missing"
    )
    parser.add_argument('arandom',
        type=str,
        action='append',
        required=True,
        help="arandom is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=True,
        help="locked option is missing"
    )
    parser.add_argument('f',
        type=float,
        required=True,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=True,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=True,
        help="q value is missing"
    )

    def get(self,name):
        answer = AnswerModel.find_by_name(name)
        if answer:
            #return survey.json()
            return answer.tojson()
        return {'message': "Answer '{}' not found in client-db".format(name)}, 404 #not found

    def post(self,name):
        if AnswerModel.find_by_name(name):
            return {'message': "answer '{}' already exist as answer in the clientdatabase for answers.".format(name)}, 400 #bad request
            #schreibe zeugs in db
        data = Answer.parser.parse_args()
        answer = AnswerModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(data['arandom']),
                                data['locked'],
                                data['f'],
                                data['p'],
                                data['q'])
        try:
            answer.save_to_db()
        except:
            return {'message': "error while inserting answer '{}'. ".format(name)}, 500
        return answer.tojson(), 201 # status created

    def delete(self,name):
        answer = AnswerModel.find_by_name(name)
        if answer:
            answer.delete_from_db()
            return {'message': "Answer '{}' deleted from client-db".format(name)}, 202 #accepted
        return {'message': "Answer '{}' not found in client-db".format(name)}, 404 #not found

class ListAnswers(Resource):
    def get(self):
        return {'answers in client-db': [ x.tojson() for x in AnswerModel.query.all()]}
