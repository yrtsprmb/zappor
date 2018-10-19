import json
from flask_restful import Resource, reqparse

from models.questions import QuestionModel

class Question(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('qid',
        type=str,
        required=True,
        help="qid is missing"
    )
    parser.add_argument('surveyid',
        type=str,
        required=True,
        help="surveyid is missing"
    )
    # parser.add_argument('qname',
    #     type=str,
    #     required=True,
    #     help="qname is missing"
    # )
    parser.add_argument('qtype',
        type=str,
        required=True,
        help="qtype missing"
    )
    parser.add_argument('qoptions',
        type=str,
        action='append',
        required=True,
        help="qoptions are missing"
    )

    def get(self,qname):
        question = QuestionModel.find_by_name(qname)
        if question:
            #return survey.json()
            return question.tojson()
        return {'message': "Question '{}' not found".format(qname)}, 404 #not found

    def post(self,qname):
        data = Question.parser.parse_args()
        #write question only in db if it belongs unique to a surveyid
        if QuestionModel.find_by_name(qname).find_by_surveyid(data['surveyid']):
             return {'message': "question '{}' already exist in database with same surveyid '{}'.".format(qname,data['surveyid'])}, 400 #bad request

        question = QuestionModel(data['qid'],
                                data['surveyid'],
                                qname,
                                data['qtype'],
                                json.dumps(data['qoptions']))
        try:
            question.save_to_db()
        except:
            return {'message': "error while inserting question '{}'. ".format(qname)}, 500
        return question.tojson(), 201 # created


class ListQuestions(Resource):
    def get(self):
        return {'questions in db': [ x.tojson() for x in QuestionModel.query.all()]}