#models/config.py
from db import db
from internal.config import serveraddress_config, serverport_config, serviceprovider_reports, serviceprovider_surveys
from internal.config import config_dsgvo, config_quizmode, config_f, config_p, config_q


class ConfigurationModel(db.Model):
    '''
    Configuration settings for the client.
    '''
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(30))
    global_f = db.Column(db.Float(precision=5))
    global_p = db.Column(db.Float(precision=5))
    global_q = db.Column(db.Float(precision=5))
    dsgvo = db.Column(db.Integer())
    quizmode = db.Column(db.Integer())
    serveraddress = db.Column(db.String(50))
    serverport = db.Column(db.Integer())
    server_get_surveys = db.Column(db.String(200))
    server_post_reports = db.Column(db.String(200))
    repeat_send_reports = db.Column(db.Integer())
    repeat_request_surveys = db.Column(db.Integer())

    def __init__(self):
        '''
        If there is no specific setting for a client, initial settings are applied.
        '''
        self.clientname = "rapporclient"
        self.global_f = config_f
        self.global_p = config_p
        self.global_q = config_q
        self.dsgvo = config_dsgvo
        self.quizmode = config_quizmode
        self.serveraddress = serveraddress_config
        self.serverport = serverport_config
        self.get_surveys = serviceprovider_surveys
        self.post_reports = serviceprovider_reports

    def __repr__(self):
        '''
        Object representaion of the client settings.
        '''
        return f" dsgvo: {bool(self.dsgvo)}, quizmode: {bool(self.quizmode)}, global_f: {self.global_f}, global_p: {self.global_p}, global_q: {self.global_q}"

    def tojson(self):
        '''
        JSON representaion of the client settings.
        '''
        return {'clientname': self.clientname, 'global_f': self.global_f, 'global_p': self.global_p,'global_q': self.global_q, 'dsgvo': bool(self.dsgvo), 'quizmode': bool(self.quizmode) }

    @classmethod
    def find(cls):
        '''
        Returns the configuration. Since the configuration is treated like a singleton, there is only one entry.
        '''
        return ConfigurationModel.query.first()

    def save_to_db(self):
        '''
        Saves configuration changes to the db.
        '''
        db.session.add(self)
        db.session.commit()
