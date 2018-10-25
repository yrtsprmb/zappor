from db import db

# Table settings in client
class ClientConfModel(db.Model):

    #global privacy settings
    __tablename__ = "clientconfiguration"
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(30))
    serveraddress = db.Column(db.String(50))
    global_f = db.Column(db.Float(precision=5))
    global_p = db.Column(db.Float(precision=5))
    global_q = db.Column(db.Float(precision=5))
    slider = db.Column(db.Float(precision=5))

    #if there is no specific privacy setting for a client, the global settings are applied
    def __init__(self, clientname, serveraddress, global_f, global_p, global_q, slider):
        self.clientname = "rapporclient"
        self.serveraddress = serveraddress
        self.global_f = global_f
        self.global_p = global_p
        self.global_q = global_q
        self.slider = slider

    #json representaion of the object
    def tojson(self):
        return {'clientname': self.clientname,
            'serveraddress': self.serveraddress,
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