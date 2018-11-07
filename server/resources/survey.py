import json
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
    # parser.add_argument('surveyname',
    #     type=str,
    #     required=False,
    #     help="name of the survey is missing"
    # )
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
         type=dict,
         action='append',
         required=True,
         help="error with questions"
    )

    #shows information about a survey by id
    def get(self, surveyname):
        survey = SurveyModel.find_survey_by_name(surveyname)
        if survey:
            #return survey.json()
            return survey.tojsonwithreports()
        return {'message': "Survey with name '{}' not found".format(surveyname)}, 404 #not found

    #generates a new survey
    #TODO: check if the parsed elements are correct, z.B. status feld

    #TODO: check if the parsed elements are correct, z.B. status feld
    def post(self, surveyname):
        if SurveyModel.find_survey_by_name(surveyname):
            return {'message': "A survey with the name '{}' already exists.".format(surveyname)}, 400 #bad request

        data = Survey.parser.parse_args()
        #survey = SurveyModel(data['surveyid'],data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions'])
        survey = SurveyModel(data['serviceprovider'],data['serviceprovider'],surveyname,data['status'],data['comment'], json.dumps(data['questions']))

        try:
            survey.save_to_db()
        except:
            return {'message': "Error while trying to save the survey"}, 500 #internal server error
        return survey.tojson(), 201 #created
        #return {'message': "A new survey was created and stored into the database"}, 201

    # def post(self, surveyname):
    #     #if SurveyModel.find_survey_by_name(surveyname):
    #     #   return {'message': "a survey with the name '{}' already exists.".format(surveyname)}, 400 #bad request
    #
    #     data = Survey.parser.parse_args()
    #     #survey = SurveyModel(data['surveyid'],data['serviceprovider'],data['surveyname'],data['status'],data['comment'], data['questions'])
    #     survey = SurveyModel(data['serviceprovider'],data['serviceprovider'],surveyname,data['status'],data['comment'], json.dumps(data['questions']))
    #
    #     #try:
    #     survey.save_to_db()
    #     #except:
    #     #    return {'message': "error while trying to save the survey"}, 500 #internal server error
    #     return survey.tojson(), 201 #created
    #     #return {'message': "A new survey was created and stored into the database"}, 201

    #deletes a survey from the database
    #TODO: when deleting survey, delete also all reports belonging to this survey

    def delete(self,surveyname):
        survey = SurveyModel.find_survey_by_name(surveyname)
        if survey:
            survey.delete_from_db()
            return {'message': "Survey with name '{}' deleted".format(surveyname)}
        return {'message': " No survey with this name"}

    # def delete(self,surveyid):
    #     survey = SurveyModel.find_survey_by_id(surveyid)
    #     if survey:
    #         survey.delete_from_db()
    #         return {'message': "Survey with id '{}' deleted".format(surveyid)}
    #     return {'message': " No survey with this id"}


# returns a list with all surveys in the datebase
class ListSurveys(Resource):
    def get(self):
        return {'surveys': [ x.tojson() for x in SurveyModel.query.all()]}


# allows to change the status of a survey in this order: created -> active -> done
class SurveyStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status',
        type=str,
        required=True,
        help="status is missing or not correct"
    )

    def put(self,surveyname):
        data = SurveyStatus.parser.parse_args()
        survey = SurveyModel.find_survey_by_name(surveyname)
        if survey is None:
            return {'message': "Can not change status, survey '{}' does not exist".format(surveyname)}, 400 #bad request

        if (survey.status == 'created' or survey.status == 'active') and (data['status'] == 'active' or data['status'] == 'done'):
            old_status = survey.status
            survey.status = data['status']
            survey.save_to_db()
            return {'message': "Status of survey '{}'  changed from '{}' to '{}' ".format(surveyname,old_status,survey.status)}, 200

        return {'message': "no changes"}, 200


##################################################################
######## Client Ressources (external ressources)
##################################################################

# check if there is a survey and send it back if yes, status must be 'active' for survey in db
class AvailableSurveys(Resource):
    def get(self):
        return {'surveys': [ x.tojsonforclient() for x in SurveyModel.query.filter_by(status='active')]}
