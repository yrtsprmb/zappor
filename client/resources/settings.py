from flask_restful import Resource, reqparse

from models.settings import SettingModel

class Settting(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('clientname',
    #     type=str,
    #     required=True,
    #     help="client needs a name"
    # )
    parser.add_argument('server',
        type=str,
        required=True,
        help="server address is missing"
    )
    parser.add_argument('global_f',
        type=float,
        required=True,
        help="global f is missing"
    )
    parser.add_argument('global_f',
        type=float,
        required=True,
        help="global f is missing"
    )
    parser.add_argument('global_p',
        type=float,
        required=True,
        help="global p is missing"
    )
    parser.add_argument('global_q',
        type=float,
        required=True,
        help="global q missing"
    )
    parser.add_argument('global_slider',
        type=float,
        action='append',
        required=False,
        help="global slider"
    )

    def get(self):
        if SettingModel.clientname == "rapporclient":
            return question.tojson()
        return {'message': "not settings for the client"}, 404 #not found

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
