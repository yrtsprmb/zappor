import json
from flask_restful import Resource

from models.client_inquiries import ClientInquiriesModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
from internal.config import global_f, global_p, global_q, global_locked
import resources.parsers
from resources.parsers import check_fpq, check_if_bits

#############################################################
# REST API for client inquiries
#############################################################
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

        # a new inquiry is created, answer, prr_answer and irr_answer will set to 0
        answer = [0]* len(data['options'])
        prr = [0]* len(data['options'])
        irr = [0]* len(data['options'])

        if not check_if_bits(answer):
            return {'message': "only 0s and 1s allowed in answers"}, 400 #bad request

        if not check_fpq(global_f, global_p, global_p):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(answer), #json.dumps(data['answer']),
                                json.dumps(prr),
                                json.dumps(irr),
                                False, #responded is False, because inquiry is created not answered
                                global_locked, #data['locked'],
                                global_f, #data['f'],
                                global_p, #data['p'],
                                global_q) #data['q'])
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while inserting inquiry with name '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 201 #created
        #return {'message': "inquiry with name '{}' sucessfully inserted.".format(name)}, 201 #created

    # change a client inquiry
    def put(self,name):
        data = resources.parsers.ParseClientInquiriesPut.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change status, inquiry '{}' does not exist".format(name)}, 400 #bad request

        #check if the format of answers is correct

        #answer must be a list of 0s and 1s
        if not check_if_bits(data['answer']):
            return {'message': "only 0s and 1s allowed in answers"}, 400 #bad request

        # user answer must have as many values as inquiry options
        if (len(json.loads(inquiry.options)) is not len(data['answer'])):
            return {'message': "Your answer must have as many values as options are available"}, 400 #bad request

        if not check_fpq(data['f'],data['p'],data['q']):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        # PRR and IRR will be only made if answer changes
        if (inquiry.answer != json.dumps(data['answer'])):

            inquiry.answer = json.dumps(data['answer'])
            # a PRR will be made after a answer is was changed
            prr = permanent_RandomizedResponse(float(data['f']),data['answer'])
            inquiry.prr_answer = json.dumps(prr)
            # a PRR will be made after a answer is was changed
            irr = instantaneous_RandomizedResponse(float(data['p']),float(data['q']),prr)
            inquiry.irr_answer = json.dumps(irr)
            # if a answer was given by the user, responded will be set to TRUE
            inquiry.responded = True

        inquiry.locked = data['locked']
        inquiry.f = data['f']
        inquiry.p = data['p']
        inquiry.q = data['q']
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while saving inquiry with name: '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 202 #accepted
        #return {'message': " inquiry '{}' changed.".format(name)}, 202 #accepted

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
# this ressources allows full access to all
# ClientInquiries values
# through the REST api
#############################################################
class TestClientInquiries(Resource):

    def post(self,name):
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exists.".format(name)}, 400 #bad request

        data = resources.parsers.ParseTestClientInquiries.parser.parse_args()

        if not (len(data['answer']) == len(data['prr_answer']) == len(data['irr_answer'])):
            return {'message': "'answer', 'prr_answer' and 'irr_answer' must have the same length"}, 400 #bad request

        if not (check_if_bits(data['answer']) and check_if_bits(data['prr_answer']) and check_if_bits(data['irr_answer'])):
            return {'message': "only 0s and 1s allowed in answer, prr_answer and irr_answer"}, 400 #bad request

        if not check_fpq(data['f'],data['p'],data['q']):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        # a PRR will be made after a answer is was changed
        prr = permanent_RandomizedResponse(float(data['f']),data['answer'])
        # a IRR will be made after every request for an inquiry
        irr = instantaneous_RandomizedResponse(float(data['p']),float(data['q']),prr)
        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(prr), #json.dumps(data['prr_answer']),
                                json.dumps(irr),#json.dumps(data['irr_answer']),
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

        if not check_fpq(data['f'],data['p'],data['q']):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        if not (check_if_bits(data['answer']) and check_if_bits(data['prr_answer']) and check_if_bits(data['irr_answer'])):
            return {'message': "only 0s and 1s allowed in answer, prr_answer and irr_answer"}, 400 #bad request

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
