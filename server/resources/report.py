#resources/report.py
import json
from flask_restful import Resource, request

from models.report import ReportModel
from models.survey import SurveyModel

import resources.parsers
from resources.parsers import check_fpq, check_if_bits

############################################
## Ressources for reports
############################################

class Report(Resource):

    def get(self,surveyid):
        '''
        a list with all reports to a specific survey in the database
        '''
        reports = [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]
        if reports == []:
            return {'message': "no reports found for surveyid '{}' ".format(surveyid)}, 400
        return {'reports': [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]}


    def post(self, surveyid):
        '''
        saves a report by it's surveyid to the database, only if f,p and q are valid
        and the survey is active.
        '''
        # print("request: ", request.args) # debug: only for testing
        if SurveyModel.find_active_survey_by_id(surveyid):
            data = resources.parsers.ParseReportsPost.parser.parse_args()

            if not check_fpq(data['f'],data['p'],data['q']):
                return {'message': "report discarded: f,p,q must have values between 0.0 and 1.0"}, 400 #bad request

            print(data)
            report = ReportModel(surveyid,
                data['prr'],
                data['irr'],
                data['f'],
                data['p'],
                data['q'],
                json.dumps(data['answers'])
            )
            try:
                report.save_to_db()
            except:
                return {'message': "error while inserting report with surveyid '{}'. ".format(surveyid)}, 500
            return report.tojson(), 201 # status created
        else:
            return {'message': "no report inserted, surveyid '{}' unknown or not active".format(surveyid)}, 400


class ListReports(Resource):
    def get(self):
        '''
        for testing: returns a list with all reports in the database.
        '''
        return {'reports': [ x.tojson() for x in ReportModel.query.all()]}
