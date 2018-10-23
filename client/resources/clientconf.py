from flask_restful import Resource, reqparse

from models.clientconf import ClientConfModel

class ClientConf(Resource):
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
    parser.add_argument('slider',
        type=float,
        required=True,
        help="global slider"
    )

    def get(self,clientname):
        configuration = ClientConfModel.find_by_name(clientname)
        if configuration:
            return configuration.tojson()
        return {'message': "Client settings not found"}, 404 #not found

    def post(self,clientname):
        data = ClientConf.parser.parse_args()
        #write question only in db if it belongs unique to a surveyid
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
