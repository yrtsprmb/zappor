import sqlite3

## internal representation of an Report

class ReportModel:
    def __init__(self, surveyid, prr, irr, f, p, q, answers):
        self.surveyid = surveyid
        self.prr = prr
        self.irr = irr
        self.f = f
        self.p = p
        self.q = q
        self.answers = answers

    # returns a json representation of the report model
    def json(self):
        return {'surveyid': self.surveyid, 'prr': self.prr, 'irr': self.irr, 'f': self.f, 'p': self.p,'q': self.q, 'answers': self.answers}


    #find a survey by its name, should be classmethod, because it returns an object of Survey Model
    @classmethod
    def find_report_by_surveyid(cls, surveyid):
        pass

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO testreport VALUES (?,?,?,?,?,?,?)"
        cursor.execute(query, (self.surveyid, self.prr, self.irr, self.f, self.p, self.q, self.answers))
        connection.commit()
        connection.close()
