#resources/server_inquiries
import json
from flask_restful import Resource

from models.server_inquiries import ServerInquiriesModel
import resources.parsers


class ServerInquiries(Resource):
    '''
    REST API for server inquiries.
    '''
    def get(self,name):
        '''
        If existing, returns a server inquiry by its name.
        '''
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            return question.tojson()
        return {'message': "Server inquiry '{}' not found".format(name)}, 404 #not found

    def delete(self,name):
        '''
        If existing, deletes a server inquiry by its name.
        '''
        question = ServerInquiriesModel.find_by_name(name)
        if question:
            question.delete_from_db()
            return {'message': "Server inquiry '{}' deleted.".format(name)}, 202 #accepted
        return {'message': "Server inquiry '{}' not found.".format(name)}, 404 #not found


class ListServerInquiries(Resource):
    def get(self):
        '''
        List all server inquiries.
        '''
        return {'inquiries': [ x.tojson() for x in ServerInquiriesModel.query.all()]}


class TestServerInquiries(Resource):
    '''
    This ressource allows full access to all server inquiry values through the REST API.
    For testing only, not for productive usage.
    '''
    def post(self,name):
        '''
        Creates a new server inquriy, if not already existing under the same name.
        This request is for testing and should be used carefully.
        '''
        data = resources.parsers.ParseTestServerInquiries.parser.parse_args()
        #write question only in db if the inquiry name is unique to a surveyid.
        if ServerInquiriesModel.find_by_name(name) and ServerInquiriesModel.find_by_surveyid(data['surveyid']):
             return {'message': "a server inquiry with name '{}' already exists belonging to surveyid '{}'.".format(name,data['surveyid'])}, 400 #bad request

        #check if description is empty
        description = ""
        if (data['qdescription'] is not None):
            description = data['qdescription']

        question = ServerInquiriesModel(data['qid'],
                                data['surveyid'],
                                data['serviceprovider'],
                                name,
                                data['type'],
                                json.dumps(data['options']),
                                description,
                                data['locked'],
                                data['quizmode'])
        try:
            question.save_to_db()
        except:
            return {'message': "error while inserting server inquiry '{}'. ".format(name)}, 500 #internal server error
        return question.tojson(), 201 #created
