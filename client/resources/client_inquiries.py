#resources/client_inquiries.py
import json
from flask_restful import Resource

from models.client_inquiries import ClientInquiriesModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
from internal.config import locked_config, configfile_f, configfile_p, configfile_q
import resources.parsers
from resources.parsers import check_fpq, check_if_bits, check_type


class ClientInquiries(Resource):
    '''
    REST API for client inquiries.
    '''
    def get(self,name):
        '''
        Returns a client inquiry by its name.
        '''
        answer = ClientInquiriesModel.find_by_name(name)
        if answer:
            return answer.tojson(), 200 #ok
        return {'message': "Inquiry with name '{}' not found.".format(name)}, 404 #not found

    def post(self,name):
        '''
        Creates a new client inquriy, if not already existing under the same name.
        '''
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exists.".format(name)}, 400 #bad request
            #schreibe zeugs in db
        data = resources.parsers.ParseClientInquiriesPost.parser.parse_args()

        #check if description is empty
        description = ""
        if (data['qdescription'] is not None):
            description = data['qdescription']

        # answer, prr_answer and irr_answer will set to 0
        answer = [0]* len(data['options'])
        prr = [0]* len(data['options'])
        irr = [0]* len(data['options'])

        #validity checks
        if not check_type(data['type']):
            return {'message': "type must be 'cbx', 'mc' or 'bool'."}, 400 #bad request

        if not check_if_bits(answer):
            return {'message': "only 0s and 1s allowed in answers"}, 400 #bad request

        if not check_fpq(configfile_f, configfile_p, configfile_q):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(answer), #json.dumps(data['answer']),
                                json.dumps(prr),
                                json.dumps(irr),
                                description,
                                False, #responded is False, because inquiry is created but not answered yet.
                                locked_config, #data['locked'],
                                configfile_f, #until first edit by the user global values are used instead of data['f'],
                                configfile_p, #until first edit by the user global values are used instead of data['p'],
                                configfile_q) #until first edit by the user global values are used instead of data['q'])
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while inserting inquiry with name '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 201 #created
        #return {'message': "inquiry with name '{}' sucessfully inserted.".format(name)}, 201 #created

    def put(self,name):
        '''
        Changes a client inquiry by its name.
        The following values can be changed by the user: answers, description, locked, f,p and q.
        '''
        data = resources.parsers.ParseClientInquiriesPut.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change status, inquiry '{}' does not exist".format(name)}, 400 #bad request

        #check if description is empty
        description = data['qdescription']
        if (data['qdescription'] is  None):
            description = inquiry.qdescription

        #check if the lengt of the answer is correct (still the same).
        if not (len(json.dumps(data['answer'])) == len(inquiry.answer)):
                    return {'message': "old and new answer must have the same amount of options"}, 400 #bad request

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

        inquiry.qdescription = description #data['qdescription']
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
        '''
        Deletes a client inquiry by its name.
        '''
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry:
            inquiry.delete_from_db()
            return {'message': "client inquiry '{}' deleted".format(name)}, 202 #accepted
        return {'message': "client inquiry '{}' not found".format(name)}, 404 #not found


class ListClientInquiries(Resource):
    def get(self):
        '''
        List all client inquiries.
        '''
        return {'inquiries': [ x.tojson() for x in ClientInquiriesModel.query.all()]}


class TestClientInquiries(Resource):
    '''
    This ressource allows full access to all ClientInquiries values through the REST API.
    For testing only, not for productive usage.
    '''
    def post(self,name):
        '''
        Creates a new client inquriy, if not already existing under the same name.
        This request is for testing and should be used carefully.
        '''
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
                                data['qdescription'],
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
        '''
        Changes a client inquiry by its name.
        This request is for testing and should be used carefully.
        '''
        data = resources.parsers.ParseTestClientInquiries.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "No changes - inquiry '{}' does not exist".format(name)}, 400 #bad request

        #check if description is empty
        description = data['qdescription']
        if (data['qdescription'] is  None):
            description = inquiry.qdescription

        if not check_fpq(data['f'],data['p'],data['q']):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        if not (check_if_bits(data['answer']) and check_if_bits(data['prr_answer']) and check_if_bits(data['irr_answer'])):
            return {'message': "only 0s and 1s allowed in answer, prr_answer and irr_answer"}, 400 #bad request

        inquiry.type = data['type']
        inquiry.options = json.dumps(data['options'])
        inquiry.answer = json.dumps(data['answer'])
        inquiry.prr_answer = json.dumps(data['prr_answer'])
        inquiry.irr_answer = json.dumps(data['irr_answer'])
        inquiry.qdescription = description #data['qdescription']
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
