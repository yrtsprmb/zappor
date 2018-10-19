from db import db

# Table surveys in client
class SettingModel(db.Model):

    #global privacy settings
    __tablename__ = "settings"
    clientname = db.Column(db.String(30))
    server = db.Column(db.String(50))
    global_f = db.Column(db.Float(precision=5))
    global_p = db.Column(db.Float(precision=5))
    global_q = db.Column(db.Float(precision=5))
    global_slider = db.Column(db.Float(10))

    def __init__(self, server, global_f, global_p, global_q, global_slider):
        self.clientname = "rapporclient"
        self.f = global_f
        self.p = global_p
        self.q = global_q
        self.slider = global_slider


    #json representaion of the object
    def tojson(self):
        return {'clientname': self.clientname,
            'f': self.global_f,
            'p': self.global_p,
            'q': self.global_q,
            'slider': self.global_slider}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
