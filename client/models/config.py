#models/config.py
from db import db
from internal.config import serveraddress_config, serverport_config, config_repeat_request_surveys, config_repeat_send_reports
from internal.config import config_dsgvo, config_f, config_p, config_q

class ConfigurationModel(db.Model):
    '''
    Configuration settings for the client.
    '''
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    serveraddress = db.Column(db.String(50))
    serverport = db.Column(db.Integer())
    server_get_surveys = db.Column(db.String(200))
    server_post_reports = db.Column(db.String(200))
    repeat_send_reports = db.Column(db.Integer())
    repeat_request_surveys = db.Column(db.Integer())
    dsgvo = db.Column(db.Integer())
    global_f = db.Column(db.Float(precision=5))
    global_p = db.Column(db.Float(precision=5))
    global_q = db.Column(db.Float(precision=5))

    def __init__(self):
        '''
        If there is no specific setting for a client, initial settings are applied.
        '''
        self.name = "rapporclient"
        self.serveraddress = configfile_server
        self.serverport = configfile_port
        self.server_get_surveys = serveraddress_config + ':' + serverport_config + '/availablesurveys'
        self.server_post_reports = serveraddress_config + ':' + serverport_config + '/reports/'
        self.repeat_send_reports = configfile_repeat_send_reports
        self.global_f = config_f
        self.global_p = config_p
        self.global_q = config_q

    def tojson(self):
        '''
        JSON representaion of the client settings.
        '''
        return {'clientname': self.clientname,
            'serveraddress': self.serveraddress,
            'serverport': self.serverport,
            'f': self.global_f,
            'p': self.global_p,
            'q': self.global_q,
            'slider': self.slider}

    @classmethod
    def find_by_name(cls, clientname):
        return ClientConfModel.query.filter_by(clientname=clientname).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
