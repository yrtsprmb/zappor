import sqlite3
from flask_restful import Resource, reqparse


############################################
######## Ressourcen nach aussen fuer die Clients
############################################

umfragen = []
umfrageids = ['helgassurvey']
offeneumfragen = []

class SurveyAvailable(Resource):
    def get(self):
        # check if there is a survey and send it back if yes, status must be 'active' for survey in db
        # aktuell gibt es nur die erste verfuegbare umfrage zurueck, und eine meldung wenn keine da.
        # todo:
        # muss die jsons ausgeben in der form von survey.json

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM surveys WHERE status='active' "

        result = cursor.execute(query)
        availablesurveys = []
        for row in result:
            availablesurveys.append({'surveyid': row[0], 'service-provider': row[1], 'questions': "muessen noch implementiert werden"})
        connection.close()
        return {'verfuegbar': availablesurveys}, 200




        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()

        if row:
            return {'survey': {'surveyid': row[0], 'surveyname': row[1]}}
        return {'message': 'Keine Umfrage gefunden'}, 404





####




#####

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
######## Ressourcen fur den Serviceprovider
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


class DeleteSurvey(Resource):
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM surveys WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': "Survey with the name '{}' deleted".format(name)}


class CreateSurvey(Resource):
    #eine Umfragen wird generiert und in die DB Gespeichert
    def post(self):
        pass
