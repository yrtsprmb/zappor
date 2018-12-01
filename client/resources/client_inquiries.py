import json
from flask_restful import Resource#, reqparse

from models.client_inquiries import ClientInquiriesModel
import resources.parsers

#REST API to Access the client questions with their answers
class ClientInquiries(Resource):

    def get(self,name):
        answer = ClientInquiriesModel.find_by_name(name)
        if answer:
            return answer.tojson(), 200 #ok
        return {'message': "Inquiry with name '{}' not found.".format(name)}, 404 #not found

    def post(self,name):
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exists.".format(name)}, 400 #bad request
            #schreibe zeugs in db
        data = resources.parsers.ParseClientInquiriesPost.parser.parse_args()
        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(data['answer']), #todo Take answer make a prr rappor and save prr_answer here
                                json.dumps(data['answer']), #todo Take prr_answer make a irr rappor and save irr_answer here
                                True,
                                data['locked'],
                                data['f'],
                                data['p'],
                                data['q'])
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while inserting inquiry with name '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 201 #created
        #return {'message': "inquiry with name '{}' sucessfully inserted.".format(name)}, 201 #created

    def put(self,name):
        data = resources.parsers.ParseClientInquiriesPut.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change status, inquiry '{}' does not exist".format(name)}, 400 #bad request

        inquiry.answer = json.dumps(data['answer'])
        inquiry.locked = data['locked']
        inquiry.f = data['f']
        inquiry.p = data['p']
        inquiry.q = data['q']
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while saving inquiry with name: '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 200 #ok
        #return {'message': " inquiry '{}' changed.".format(name)}, 200 #ok

    def delete(self,name):
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry:
            inquiry.delete_from_db()
            return {'message': "client inquiry '{}' deleted".format(name)}, 202 #accepted
        return {'message': "client inquiry '{}' not found".format(name)}, 404 #not found


#############################################################
# list all client inquiries
#############################################################
class ListClientInquiries(Resource):
    def get(self):
        return {'inquiries': [ x.tojson() for x in ClientInquiriesModel.query.all()]}


#############################################################
# this ressource allows full access to all values
# through the REST api
#############################################################
class TestClientInquiries(Resource):

    def post(self,name):
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exists.".format(name)}, 400 #bad request

        data = resources.parsers.ParseTestClientInquiries.parser.parse_args()
        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(data['prr_answer']),
                                json.dumps(data['irr_answer']),
                                data['responded'],
                                data['locked'],
                                data['f'],
                                data['p'],
                                data['q'])
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while inserting inquiry with name '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 201 #created

    def put(self,name):
        data = resources.parsers.ParseTestClientInquiries.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "No changes - inquiry '{}' does not exist".format(name)}, 400 #bad request

        inquiry.type = data['type']
        inquiry.options = json.dumps(data['options'])
        inquiry.answer = json.dumps(data['answer'])
        inquiry.prr_answer = json.dumps(data['prr_answer'])
        inquiry.irr_answer = json.dumps(data['irr_answer'])
        inquiry.responded = data['responded']
        inquiry.locked = data['locked']
        inquiry.f = data['f']
        inquiry.p = data['p']
        inquiry.q = data['q']

        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while editing inquiry with name: '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 202 #accepted
