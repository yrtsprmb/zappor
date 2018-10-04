import sqlite3

## internal representation

class SurveyModel:
    def __init__(self, surveyid, serviceprovider, surveyname, status, comment, questions):
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.surveyname = surveyname
        self.status = status
        self.comment = comment
        self.questions = questions

    # returns a json representation of the survey model
    def json(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'comment': self.comment, 'questions': self.questions}


    #find a survey by its name, returns an object of Survey Model
    @classmethod
    def find_survey_by_name(cls, surveyname):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM umfragen WHERE surveyname=?"
        result = cursor.execute(query, (surveyname,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row) #works also cls(*row)


    def createsurvey(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO umfragen VALUES (?,?,?,?,?,?)"
        cursor.execute(query, (self.surveyid, self.serviceprovider, self.surveyname, self.status, self.comment, self.questions))

        connection.commit()
        connection.close()
