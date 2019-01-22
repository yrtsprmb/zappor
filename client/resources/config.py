#resources/config.py
from flask_restful import Resource
from models.config import ConfigurationModel
import resources.parsers


class Configuration(Resource):

    # def get(self,clientname):
    #     cnfg = ConfigurationModel.find_by_name(clientname)
    #     if cnfg:
    #         return cnfg.tojson()
    #     return {'message': "Client settings not found"}, 404 #not found

    def get(self):
        cnfg = ConfigurationModel.find()
        if cnfg:
            return cnfg.tojson()
        return {'message': "Client settings not found"}, 404 #not found


    def post(self,clientname):
        data = resources.parsers.ParseConfiguration.parser.parse_args()
        #data = ClientConf.parser.parse_args()

        if ConfigurationModel.find_by_name(clientname):
             return {'message': "client with name '{}' already exist in database.".format(clientname)}, 400 #bad request

        # self.clientname = "rapporclient"
        # self.global_f = config_f
        # self.global_p = config_p
        # self.global_q = config_q
        # self.dsgvo = config_dsgvo
        # self.serveraddress = serveraddress_config
        # self.serverport = serverport_config
        # self.get_surveys = serviceprovider_surveys
        # self.post_reports = serviceprovider_reports

        cnfg = ConfigurationModel(clientname,
                                data['serveraddress'],
                                data['global_f'],
                                data['global_p'],
                                data['global_q'],
                                data['dsgvo'],
                                data['serveraddress'],
                                data['serverport'],
                                data['get_surveys'],
                                data['post_reports'])
        try:
            cnfg.save_to_db()
        except:
            return {'message': "error while setting personal settings for '{}'. ".format(clientname)}, 500
        return cnfg.tojson(), 201 # created
