from flask_restful import Resource
from models.config import ConfigurationModel
import resources.parsers


class ClientConf(Resource):

    def get(self,clientname):
        configuration = ClientConfModel.find_by_name(clientname)
        if configuration:
            return configuration.tojson()
        return {'message': "Client settings not found"}, 404 #not found

    def post(self,clientname):
        data = resources.parsers.ParseClientConf.parser.parse_args()
        #data = ClientConf.parser.parse_args()

        if ClientConfModel.find_by_name(clientname):
             return {'message': "client with name '{}' already exist in database.".format(clientname)}, 400 #bad request

        configuration = ClientConfModel(clientname,
                                data['serveraddress'],
                                data['global_f'],
                                data['global_p'],
                                data['global_q'],
                                data['slider'])
        try:
            configuration.save_to_db()
        except:
            return {'message': "error while setting personal settings for '{}'. ".format(clientname)}, 500
        return configuration.tojson(), 201 # created
