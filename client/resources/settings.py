from flask_restful import Resource, reqparse

from models.settings import SettingModel

class Setttings(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('clientname',
    #     type=str,
    #     required=True,
    #     help="client needs a name"
    # )
    parser.add_argument('serveraddress',
        type=str,
        required=True,
        help="server address is missing"
    )
    parser.add_argument('global_f',
        type=float,
        required=True,
        help="global f is missing"
    )
    parser.add_argument('global_p',
        type=float,
        required=True,
        help="global p is missing"
    )
    parser.add_argument('global_q',
        type=float,
        required=True,
        help="global q missing"
    )
    parser.add_argument('global_slider',
        type=float,
        action='append',
        required=False,
        help="global slider"
    )

    def get(self,clientname):
        setting = SettingModel.find_by_name(clientname)
        if setting:
            return setting.tojson()
        return {'message': "Client settings not found"}, 404 #not found

    def post(self,clientname):
        data = Settings.parser.parse_args()
        #write question only in db if it belongs unique to a surveyid
        if SettingModel.find_by_name(clientname):
             return {'message': "client with name '{}' already exist in database.".format(clientname)}, 400 #bad request

        setting = SettingModel(clientname,
                                data['serveraddress'],
                                data['global_f'],
                                data['global_p'],
                                data['global_q'],
                                data['global_slider'])
        try:
            setting.save_to_db()
        except:
            return {'message': "error while setting personal settings for '{}'. ".format(clientname)}, 500
        return setting.tojson(), 201 # created
