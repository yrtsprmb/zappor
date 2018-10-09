from flask_restful import Resource, reqparse
from models.survey import SurveyModel

##################################################################
######## Ressources for the service provider (internal ressources)
##################################################################

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

    #shows information about a survey by id
    def get(self, surveyid):
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey:
            return survey.json()
        return {'message': "Survey with id '{}' not found".format(surveyid)}, 404 #not found

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

    #deletes a survey from the database
    def delete(self,surveyid):
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey:
            survey.delete_survey_from_db()
            return {'message': "Survey with id '{}' deleted".format(surveyid)}
        return {'message': " No survey with this id"}


# returns a list with all surveys in the datebase
class SurveyList(Resource):
    def get(self):
        return {'surveys': [ x.json() for x in SurveyModel.query.all()]}


# allows to change the status of a survey in this order: created -> active -> done
class SurveyStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status',
        type=str,
        required=True,
        help="status is missing or not correct"
    )

    def put(self,surveyid):
        data = SurveyStatus.parser.parse_args()
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey is None:
            return {'message': "can not change status, surveyid '{}' does not exist".format(surveyid)}, 400 #bad request

        if (survey.status == 'created' or survey.status == 'active') and (data['status'] == 'active' or data['status'] == 'done' ):
            old_status = survey.status
            survey.status = data['status']
            survey.save_survey_to_db()
            return {'message': "surveyid '{}' status changed from '{}' to '{}' ".format(surveyid,old_status,survey.status)}, 200

        return {'message': "no changes"}, 200


##################################################################
######## Client Ressources (external ressources)
##################################################################

# check if there is a survey and send it back if yes, status must be 'active' for survey in db
class SurveyAvailable(Resource):
    def get(self):
        return {'surveys': [ x.jsonforclient() for x in SurveyModel.query.filter_by(status='active')]}
