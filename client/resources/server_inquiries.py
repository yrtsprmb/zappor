import json
from flask_restful import Resource, reqparse

from models.server_inquiries import ServerInquiriesModel

class ServerInquiries(Resource):
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
    parser.add_argument('serviceprovider',
        type=str,
        required=True,
        help="serviceprovider is missing"
    )
    # parser.add_argument('qname',
    #     type=str,
    #     required=True,
    #     help="qname is missing"
    # )
    parser.add_argument('type',
        type=str,
        required=True,
        help="type missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=True,
        help="options are missing"
    )

    def get(self,name):
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            return question.tojson()
        return {'message': "Question '{}' not found".format(name)}, 404 #not found

    def post(self,name):
        data = ServerInquiries.parser.parse_args()
        #write question only and only in db if it is unique to a surveyid
        if ServerInquiriesModel.find_by_name(name): #find_by_surveyid(data['surveyid'])
             return {'message': "question '{}' already exist in database with same surveyid '{}'.".format(name,data['surveyid'])}, 400 #bad request

        question = ServerInquiriesModel(data['qid'],
                                data['surveyid'],
                                data['serviceprovider'],
                                name,
                                data['type'],
                                json.dumps(data['options']))
        try:
            question.save_to_db()
        except:
            return {'message': "error while inserting question '{}'. ".format(name)}, 500
        return question.tojson(), 201 # created

    def delete(self,name):
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            question.delete_from_db()
            return {'message': "Question '{}' deleted from client-db".format(name)}, 202 #accepted
        return {'message': "Question '{}' not found in client-db".format(name)}, 404 #not found


class ListServerInquiries(Resource):
    def get(self):
        return {'inquiries': [ x.tojson() for x in ServerInquiriesModel.query.all()]}
