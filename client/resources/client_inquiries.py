#resources/client_inquiries.py
import json
from flask_restful import Resource
from models.client_inquiries import ClientInquiriesModel
from models.config import ConfigurationModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
from internal.config import config_locked, config_f, config_p, config_q
import resources.parsers
from resources.parsers import check_fpq, check_if_bits, check_type, check_bool, check_mc


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
            print("IRR before")
            print(answer.irr_answer)
            prr = json.loads(answer.prr_answer)
            new_irr = instantaneous_RandomizedResponse(answer.p,answer.q,prr)
            answer.irr_answer = json.dumps(new_irr)
            #answer.save_to_db() # this would change an object with a GET-Request which is not allowed by the REST Definition
            print("IRR afterwards")
            print(answer.irr_answer)

            return answer.tojson(), 200 #ok
        return {'message': "Inquiry with name '{}' not found.".format(name)}, 404 #not found

    def post(self,name):
        '''
        Creates a new client inquriy, if not already existing under the same name.
        '''
        cnfg = ConfigurationModel.find()
        if cnfg is None or cnfg.dsgvo != 1:
                return {'message': "Configuration error. Check your GDPR/DSGVO settings."}, 400 #bad request

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

        if (data['type'] == 'bool' and len(data['options']) != 2):
            return {'message': "when type 'bool' is chosen, only 2 answer options are possible."}, 400 #bad request

        if not check_if_bits(answer):
            return {'message': "only 0s and 1s allowed in answers"}, 400 #bad request

        if not check_fpq(config_f, config_p, config_q):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        inquiry = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(answer), #json.dumps(data['answer']),
                                json.dumps(prr),
                                json.dumps(irr),
                                description,
                                False, #responded is False, because inquiry is created but not answered yet.
                                config_locked, #data['locked'],
                                cnfg.global_f, #config_f, until first edit by the user global values are used instead of data['f'],
                                cnfg.global_p, #config_p, #until first edit by the user global values are used instead of data['p'],
                                cnfg.global_q) #config_q) #until first edit by the user global values are used instead of data['q'])
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
        cnfg = ConfigurationModel.find()
        if cnfg is None or cnfg.dsgvo != 1:
                return {'message': "Configuration error. Check your GDPR/DSGVO settings."}, 400 #bad request

        data = resources.parsers.ParseClientInquiriesPut.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change status, inquiry '{}' does not exist".format(name)}, 400 #bad request

        #check if description is empty
        description = data['qdescription']
        if (data['qdescription'] is  None):
            description = inquiry.qdescription

        #check if the lengt of the answer is correct (still the same).
        if not (len(data['answer']) == len(json.loads(inquiry.answer))):
            print("laenge")
            print(len(data['answer']))
            print(len(json.loads(inquiry.answer)))
            return {'message': "old and new answer must have the same amount of options."}, 400 #bad request

        #check bool
        if not check_bool(inquiry.type,data['answer']):
            return {'message': "error: give a correct answer for type 'bool'."}, 400 #bad request

        #check mc
        if not check_mc(inquiry.type,data['answer']):
            return {'message': "error: only one answer options is allowed for mc questions."}, 400 #bad request

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
        Deletes a client inquiry by it's name.
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
