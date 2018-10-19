from db import db

# Table surveys in client
class SurveyModel(db.Model):

    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(100))
    longterm = db.Column(db.Integer(1))
    processed = db.Column(db.Integer(1))

    def __init__(self, surveyid, longterm, processed):
        self.surveyid = surveyid
        self.longterm = longterm
        self.processed = processed

    #json representaion of a survey object
    def tojson(self):
        return {'surveyid': self.surveyid, 'longterm': self.longterm, 'processed': self.processed}

    @classmethod
    def find_by_surveyid(cls, surveyid):
        return cls.query.filter_by(surveyid=surveyid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
