#resouces/surveys.py

import json
from flask_restful import Resource, reqparse
from models.surveys import SurveyModel
import resources.parsers
from resources.parsers import check_status, check_incoming_survey


class Survey(Resource):
    '''
    REST API for surveys.
    '''
    def get(self, surveyname):
        '''
        Server REST resource.
        Shows a survey by its surveyname.
        '''
        survey = SurveyModel.find_survey_by_name(surveyname)
        if survey:
            return survey.tojsonwithreports(), 200 #ok
        return {'message': "Survey with name '{}' not found".format(surveyname)}, 404 #not found

    def post(self, surveyname):
        '''
        Server REST Resource:
        Creates a new survey by its surveyname.
        '''
        if SurveyModel.find_survey_by_name(surveyname):
            return {'message': "A survey with the name '{}' already exists.".format(surveyname)}, 400 #bad request

        data = resources.parsers.ParseSurveysPost.parser.parse_args()

        if not check_status(data['status']):
            return {'message': "wrong status. must be 'created', 'active', or 'done'."}, 400 #bad request

        questionlist = data['questions']
        print(data['questions'])
        print(type(data['questions']))

        if check_incoming_survey(questionlist):
            print("Helga Testet")

        #check_type(data['status']):

        survey = SurveyModel(data['serviceprovider'],
                                data['serviceprovider'], # surveyid will be auto generated in the survey model
                                surveyname,
                                data['status'],
                                data['sdescription'],
                                json.dumps(data['questions']))
        try:
            survey.save_to_db()
        except:
            return {'message': "Error while trying to save the survey."}, 500 #internal server error
        return survey.tojson(), 201 #created
        #return {'message': "A new survey was created and stored into the database"}, 201 #created

    def put(self,surveyname):
        '''
        Server REST resource:
        Changes the status of a survey.
        After a survey is created, only it's status can be changed from 'created' -> 'active' -> 'done'.
        '''
        data = resources.parsers.ParseSurveysPut.parser.parse_args()
        survey = SurveyModel.find_survey_by_name(surveyname)

        if survey is None:
            return {'message': "Can not change status, survey '{}' does not exist".format(surveyname)}, 400 #bad request

        if not check_status(data['status']):
            return {'message': "wrong status. must be 'created', 'active', or 'done'."}, 400 #bad request

        if (survey.status == 'created' or survey.status == 'active') and (data['status'] == 'active' or data['status'] == 'done'):
            old_status = survey.status
            survey.status = data['status']
            survey.save_to_db()
            return {'message': "Status of survey '{}'  changed from '{}' to '{}' ".format(surveyname,old_status,survey.status)}, 200 #ok

        return {'message': "no changes"}, 200 #ok

    def delete(self,surveyname):
        '''
        Server REST resource:
        Deletes a survey by its name.
        '''
        survey = SurveyModel.find_survey_by_name(surveyname)
        if survey:
            try:
                survey.delete_from_db()
            except:
                return {'message': "Error while trying to delete the survey."}, 500 #internal server error

            return {'message': "Survey with name '{}' deleted.".format(surveyname)}, 202 #accepted
        return {'message': " No survey with this name."}, 400 #bad request


class ListSurveys(Resource):
    def get(self):
        '''
        Server REST resource:
        Lists all  existing surveys.
        '''
        return {'surveys': [ x.tojson() for x in SurveyModel.query.all()]}


class AvailableSurveys(Resource):
    def get(self):
        '''
        Client REST resource:
        Shows all available surveys.
        A survey for a client is available if its status is 'active'.
        '''
        return {'surveys': [ x.tojsonforclient() for x in SurveyModel.query.filter_by(status='active')]}
