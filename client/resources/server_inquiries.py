import json
from flask_restful import Resource

from models.server_inquiries import ServerInquiriesModel
import resources.parsers

class ServerInquiries(Resource):

    def get(self,name):
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            return question.tojson()
        return {'message': "Server inquiry '{}' not found".format(name)}, 404 #not found

    # def post(self,name):
    #     data = ServerInquiries.parser.parse_args()
    #     #write question only in db if it is unique to a surveyid
    #     if ServerInquiriesModel.find_by_name(name) and ServerInquiriesModel.find_by_surveyid(data['surveyid']):
    #          return {'message': "a question '{}' already exist under the surveyid '{}'.".format(name,data['surveyid'])}, 400 #bad request
    #
    #     question = ServerInquiriesModel(data['qid'],
    #                             data['surveyid'],
    #                             data['serviceprovider'],
    #                             name,
    #                             data['type'],
    #                             json.dumps(data['options']))
    #     try:
    #         question.save_to_db()
    #     except:
    #         return {'message': "error while inserting question '{}'. ".format(name)}, 500
    #     return question.tojson(), 201 # created

    def delete(self,name):
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            question.delete_from_db()
            return {'message': "Server inquiry '{}' deleted.".format(name)}, 202 #accepted
        return {'message': "Server inquiry '{}' not found.".format(name)}, 404 #not found


class ListServerInquiries(Resource):
    def get(self):
        return {'inquiries': [ x.tojson() for x in ServerInquiriesModel.query.all()]}


class TestServerInquiries(Resource):
    def post(self,name):
        #data = ServerInquiries.parser.parse_args()
        data = resources.parsers.ParseTestServerInquiries.parser.parse_args()
        #write question only in db if it is unique to a surveyid
        if ServerInquiriesModel.find_by_name(name) and ServerInquiriesModel.find_by_surveyid(data['surveyid']):
             return {'message': "a server inquiry with name '{}' already exists belonging to surveyid '{}'.".format(name,data['surveyid'])}, 400 #bad request

        question = ServerInquiriesModel(data['qid'],
                                data['surveyid'],
                                data['serviceprovider'],
                                name,
                                data['type'],
                                json.dumps(data['options']))
        try:
            question.save_to_db()
        except:
            return {'message': "error while inserting server inquiry '{}'. ".format(name)}, 500 #internal server error
        return question.tojson(), 201 #created
