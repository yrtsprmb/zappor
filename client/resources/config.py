#resources/config.py
from flask_restful import Resource
from models.config import ConfigurationModel
import resources.parsers
from resources.parsers import check_fpq


class Configuration(Resource):
    '''
    REST API for client configuration.
    '''
    def get(self):
        '''
        Returns the configuration in JSON format.
        '''
        cnfg = ConfigurationModel.find()
        if cnfg:
            return cnfg.tojson()
        return {'message': "Client settings not found"}, 404 #not found

    def put(self):
        '''
        Allows to change the configuration. There is no post request, because the configuration is treated as singleton.
        '''
        data = resources.parsers.ParseConfiguration.parser.parse_args()
        cnfg = ConfigurationModel.find()
        if cnfg is None:
            return {'message': "No configuration available"}, 400 #bad request

        if not check_fpq(data['global_f'],data['global_p'],data['global_q']):
            return {'message': "Global f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        cnfg.global_f = data['global_f']
        cnfg.global_p = data['global_p']
        cnfg.global_q = data['global_q']
        cnfg.dsgvo = data['dsgvo']
        cnfg.quizmode = data['quizmode']

        try:
            cnfg.save_to_db()
        except:
            return {'message': "Error while setting configuration data."}, 500
        return cnfg.tojson(), 201 # created
