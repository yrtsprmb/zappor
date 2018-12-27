#models.config.py
from db import db
from internal.config import serviceprovider_config


class ConfigurationModel(db.Model):
    '''
    Configuration settings for the server.
    '''
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    serviceprovider = db.Column(db.String(50))

    def __init__(self, serviceprovider):
        '''
        If there is no specific setting for a server, initial settings are applied.
        '''
        self.name = "rapporserver"
        self.serviceprovider = serviceprovider_config

    def tojson(self):
        '''
        JSON representation of the settings.
        '''
        return {'name': self.name, 'serviceprovider': self.serviceprovider}

    @classmethod
    def find_by_name(cls, name):
        '''
        Find settings by the name of the server.
        '''
        return ClientConfModel.query.filter_by(name=name).first()

    def save_to_db(self):
        '''
        Saves changes of settings to the db.
        '''
        db.session.add(self)
        db.session.commit()

    # def delete_from_db(self):
    #     '''
    #     Settings should be only overwritten, not deleted.
    #     '''
    #     db.session.delete(self)
    #     db.session.commit()
