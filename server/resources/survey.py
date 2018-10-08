#import sqlite3
from flask_restful import Resource, reqparse
from models.survey import SurveyModel

############################################
######## Ressourcen nach aussen fuer die Clients
############################################

class Survey(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument('surveyid',
    #    type=str,
    #    required=True,
    #    help="surveyid is missing"
    #)
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

    #generates a new survey
    def post(self, surveyid):
        if SurveyModel.find_survey_by_id(surveyid):
            return {'message': "a survey with the surveyid '{}' already exists.".format(surveyid)}, 400 #bad request

        data = Survey.parser.parse_args()
        #survey = SurveyModel(data['surveyid'],data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions']) #todo
        survey = SurveyModel(surveyid,data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions']) #todo

        try:
            survey.save_survey_to_db()
        except:
            return {'message': "error while trying to save the survey"}, 500 #internal server error
        return survey.json(), 201 #created
        #return {'message': "A new survey was created and stored into the database"}, 201

    #allows to change the status of a survey, from: created -> active -> finished
    def put(self,surveyid):
        data = request.get_json() #uebergibt python payolad an variable data
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey is None:
            return {'message': "can not change status,survey does not exist"}, 500 #internal server error
            #item = ItemModel(name, data['price']) # da nichts gefunden wurde, wird ein neues item kreiert

        if survey.status == 'created' and data['status'] == 'active':
            survey.status = data['status']
            survey.save_survey_to_db()
            return {'message': "changed status from surveyid '{}': created -> active".format(surveyid)}, 200

            pass

        if survey.status == 'active':
            pass

        if survey.status == 'finished':
            pass


    #deletes a survey from the database
    def delete(self,surveyid):
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey:
            survey.delete_survey_from_db()
            return {'message': "Survey with id '{}' deleted".format(surveyid)}
        return {'message': " No survey with this id"}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM surveys WHERE surveyid=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        # return {'message': "Survey with id '{}' deleted".format(name)}


# returns a list with all surveys in the datebase
class SurveyList(Resource):
    def get(self):
        return {'surveys': [ x.json() for x in SurveyModel.query.all()]}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM surveys"
        # result = cursor.execute(query)
        # surveys = []
        # for row in result:
        #     surveys.append({'surveyid': row[0], 'serviceprovider': row[1], 'surveyname': row[2], 'status': row[3], 'comment': row[4], 'questions': row[5]})
        #
        # connection.close()
        # return {'surveys in database': surveys}

# check if there is a survey and send it back if yes, status must be 'active' for survey in db
class SurveyAvailable(Resource):
    def get(self):
        return {'surveys': [ x.jsonforclient() for x in SurveyModel.query.filter_by(status='active')]}
        #UserModel.query.filter_by(username=username).first()

        #
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM surveys WHERE status='active' "
        #
        # result = cursor.execute(query)
        # availablesurveys = []
        # for row in result:
        #     availablesurveys.append({'surveyid': row[0], 'service-provider': row[1], 'questions': row[5]})
        # connection.close()
        # return {'surveys': availablesurveys}, 200
        #
        # result = cursor.execute(query)
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return {'survey': {'surveyid': row[0], 'surveyname': row[1]}}
        # return {'message': 'Keine Umfrage gefunden'}, 404







############################################
######## Ressourcen nach innen fuer den Serviceprovider
############################################
