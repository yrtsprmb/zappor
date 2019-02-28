#resources/reports.py
import json
from flask_restful import Resource, request

from models.reports import ReportModel
from models.surveys import SurveyModel

import resources.parsers
from resources.parsers import check_fpq, check_incoming_report


class Report(Resource):

    def get(self,surveyid):
        '''
        Server REST resource.
        Returns list with all reports to a specific survey in the database.
        '''
        reports = [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]
        if reports == []:
            return {'message': "no reports found for surveyid '{}' ".format(surveyid)}, 400 #bad request
        return {'reports': [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]}, 200 #ok

    def post(self, surveyid):
        '''
        Client/public REST resource.
        Saves a report sent by a client, only if data is valid and the referenced survey is active.
        '''
        # print("request: ", request.args) # debug: only for testing
        if SurveyModel.find_active_survey_by_id(surveyid):
            data = resources.parsers.ParseReportsPost.parser.parse_args()
            survey = SurveyModel.find_survey_by_id(surveyid)

            # validity: check if global fpq values are correct.
            if not check_fpq(data['f'],data['p'],data['q']):
                return {'message': "report discarded: f,p,q must have values between 0.0 and 1.0"}, 400 #bad request

            report = ReportModel(surveyid,
                data['prr'],
                data['irr'],
                data['f'],
                data['p'],
                data['q'],
                json.dumps(data['answers'])
            )
            # check if type is correct, check if length of answer is correct
            if check_incoming_report(report,survey):
                print("report ok")
                try:
                    report.save_to_db()
                except:
                    return {'message': "error while inserting report with surveyid '{}'. ".format(surveyid)}, 500 #internal server error
                return report.tojson(), 201 #created

        return {'message': "report not accecpted. Incoming data not valid or survey not existing."}, 400 #bad request

    def delete(self,surveyid):
        '''
        Server REST resource for testing:
        Deletes all reports for one surveyid TODO.
        '''
        return {'message': " not impemented."}, 200 #ok


class ListReports(Resource):
    def get(self):
        '''
        Server REST resource for testing:
        Returns a list with all reports in the database.
        '''
        return {'reports': [ x.tojson() for x in ReportModel.query.all()]}, 200 #ok
