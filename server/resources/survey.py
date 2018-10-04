import sqlite3
from flask_restful import Resource, reqparse

from models.survey import SurveyModel
#from models.survey import SurveyModel #wird noch nicht benoetigt


############################################
######## Ressourcen nach aussen fuer die Clients
############################################

#umfragen = []
#umfrageids = ['helgassurvey']
#offeneumfragen = []


class Survey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('surveyid',
        type=str,
        required=True,
        help="surveyid is missing"
    )
    parser.add_argument('serviceprovider',
        type=str,
        required=True,
        help="serviceprovider is missing"
    )
    parser.add_argument('surveyname',
        type=str,
        required=True,
        help="name of the survey is missing"
    )
    parser.add_argument('status',
        type=str,
        required=True,
        help="status value is missing"
    )
    parser.add_argument('comment',
        type=str,
        required=True,
        help="no comment"
    )
    parser.add_argument('questions',
        type=str,
        required=True,
        help="error with questions"
    )

    #eine Umfragen wird generiert und in die DB Gespeichert
    def post(self, name):
        if SurveyModel.find_survey_by_name(name):
            return {'message': "a survey with name '{}' already exists.".format(name)}, 400 #bad request

        data = Survey.parser.parse_args()
        survey = SurveyModel(data['surveyid'],data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions']) #todo

        try:
            survey.createsurvey()
        except:
            return {'message': "error while trying to gerneate survey '{}'".format(surveyname)}, 500 #internal server error
        return survey.json(), 201 #created


    #deletes an survey from the Database
    def delete(self,name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM surveys WHERE surveyid=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': "Survey with id '{}' deleted".format(name)}


# returns a list with all surveys in the datebase
class SurveyList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM surveys"
        result = cursor.execute(query)
        surveys = []
        for row in result:
            surveys.append({'surveyid': row[0], 'serviceprovider': row[1], 'surveyname': row[2], 'status': row[3], 'comment': row[4], 'questions': row[5]})

        connection.close()
        return {'surveys in database': surveys}

# check if there is a survey and send it back if yes, status must be 'active' for survey in db
class SurveyAvailable(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM surveys WHERE status='active' "

        result = cursor.execute(query)
        availablesurveys = []
        for row in result:
            availablesurveys.append({'surveyid': row[0], 'service-provider': row[1], 'questions': row[5]})
        connection.close()
        return {'surveys': availablesurveys}, 200

        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()

        if row:
            return {'survey': {'surveyid': row[0], 'surveyname': row[1]}}
        return {'message': 'Keine Umfrage gefunden'}, 404







############################################
######## Ressourcen nach innen fuer den Serviceprovider
############################################
