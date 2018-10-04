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
        type=float,
        required=False,
        help="no comment"
    )
    parser.add_argument('questions',
        type=float,
        required=True,
        help="q value is missing"
    )

    #eine Umfragen wird generiert und in die DB Gespeichert
    def post(self, surveyname):
        if SurveyModel.find_survey_by_name(surveyname):
            return {'message': "a survey with name '{}' already exists.".format(surveyname)}, 400 #bad request

        data = Survey.parser.parse_args()
        survey = SurveyModel(data['surveyid'],data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions']) #todo

        try:
            survey.createsurvey()
        except:
            return {'message': "erro while trying to gerneate survey '{}'".format(surveyname)}, 500 #internal server error
        return survey.json(), 201 #created


    #deletes an survey from the Database
    def delete(self,surveyname):
        if SurveyModel.find_survey_by_name(surveyname):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM umfragen WHERE surveyname=?"
            cursor.execute(query, (surveyname,))

            connection.commit()
            connection.close()
            return {'message': "Survey with name '{}' deleted".format(surveyname)}
        return {'message': 'Survey not in db'}, 400


# check if there is a survey and send it back if yes, status must be 'active' for survey in db
# aktuell gibt es nur die erste verfuegbare umfrage zurueck, und eine meldung wenn keine da.
# todo:
# muss die jsons ausgeben in der form von survey.json
class SurveyAvailable(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM surveys WHERE status='active' "

        result = cursor.execute(query)
        availablesurveys = []
        for row in result:
            availablesurveys.append({'surveyid': row[0], 'service-provider': row[1], 'questions': "muessen noch implementiert werden"})
        connection.close()
        return {'surveys': availablesurveys}, 200

        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()

        if row:
            return {'survey': {'surveyid': row[0], 'surveyname': row[1]}}
        return {'message': 'Keine Umfrage gefunden'}, 404



##### Schnittstelle nach aussen, ueber diese werden Umfragen entgegengenommen und in die DB gespeichert,
##### falls die surveyid in der DB vorhanden ist
class ReceiveSurvey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('f',
        type=float,
        required=True,
        help="RAPPOR value f missing/not correct"
    )
    parser = reqparse.RequestParser()
    parser.add_argument('p',
        type=float,
        required=True,
        help="RAPPOR value p missing/not correct"
    )
    parser = reqparse.RequestParser()
    parser.add_argument('q',
        type=float,
        required=True,
        help="RAPPOR value q missing/not correct"
    )
    # if survey exists, save it to the id in the database, if not discard
    def post(self, name):
        #if next(filter(lambda x: x['surveyid'] == item,items), none)
        data = request.get_json()
        survey = {'surveyid': data['surveyid'], 'service-provider': data['service-provider'], 'questions': data['questions']}
        umfragen.append(survey)
        return survey, 201




############################################
######## Ressourcen nach innen fuer den Serviceprovider
############################################

class ManageReports(Resource):
    #Umfragen werden verwaltet
    def get(self):
        # zeigt alle Umfragen an, die in DB liegen
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM surveys"
        result = cursor.execute(query)
        umfragen = []
        for row in result:
            umfragen.append({'ID der Umfrage': row[0], 'Radiosender': row[1], 'Titel der Umfrage': row[2], 'status der umfrage': row[3]})
        connection.close()
        return {'vorhandene Umfragen': umfragen}


# loescht ein survey aus der Datenbank durch den Serviceprovider
class DeleteSurvey(Resource):
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM surveys WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': "Survey with the name '{}' deleted".format(name)}


# erstellt eine survey durch den serviceprovider
class CreateSurvey(Resource):
    #eine Umfragen wird generiert und in die DB Gespeichert
    def post(self):
        pass

# gibt eine Liste aller
class SurveyList(Resource):
    pass
