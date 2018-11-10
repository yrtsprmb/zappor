import json
from flask_restful import Resource, reqparse

from models.client_inquiries import ClientInquiriesModel

#REST API to Access the client questions with their answers
class ClientInquiries(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=False,
        help="name error through parsing"
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
    parser.add_argument('randomanswer',
        type=str,
        action='append',
        required=True,
        help="randomanswer is missing"
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
        answer = ClientInquiriesModel.find_by_name(name)
        if answer:
            return answer.tojson()
        return {'message': "Inquiry with name'{}' not found in client-db".format(name)}, 404 #not found

    def post(self,name):
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exist in client-db.".format(name)}, 400 #bad request
            #schreibe zeugs in db
        data = ClientInquiries.parser.parse_args()
        answer = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(data['randomanswer']),
                                data['locked'],
                                data['f'],
                                data['p'],
                                data['q'])
        try:
            answer.save_to_db()
        except:
            return {'message': "error while inserting answer '{}'.".format(name)}, 500
        return answer.tojson(), 201 # status created


    def put(self,name):
        if ClientInquiriesModel.find_by_name(name):
            data = ClientInquiries.parser.parse_args()
            answer = ClientInquiriesModel(name,
                                    data['type'],
                                    json.dumps(data['options']),
                                    json.dumps(data['answer']),
                                    json.dumps(data['randomanswer']),
                                    data['locked'],
                                    data['f'],
                                    data['p'],
                                    data['q'])
            try:
                answer.save_to_db()
            except:
                return {'message': "error while inquiry with name: '{}'.".format(name)}, 500
            return answer.tojson(), 201 # status created

        return {'message': "No client inquiry with name '{}' in db.".format(name)}, 400 #bad request


    def delete(self,name):
        answer = ClientInquiriesModel.find_by_name(name)
        if answer:
            answer.delete_from_db()
            return {'message': "answer '{}' deleted".format(name)}, 202 #accepted
        return {'message': "answer '{}' not found".format(name)}, 404 #not found

class ListClientInquiries(Resource):
    def get(self):
        return {'inquiries': [ x.tojson() for x in ClientInquiriesModel.query.all()]}
