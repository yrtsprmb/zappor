#resources/reports.py
import json
from flask_restful import Resource
from models.reports import ReportModel
import resources.parsers
from resources.parsers import check_fpq, check_if_bits


class Report(Resource):
    '''
    This ressource is for testing. Reports are generated automatically.
    '''
    def get(self,surveyid):
        '''
        Returns a report by it's surveyid.
        '''
        reports = ReportModel.find_by_surveyid(surveyid)
        if reports:
            return {'reports': [ x.tojson() for x in ReportModel.find_by_surveyid(surveyid).query.all()]}
        return {'message': "report not found"}, 404 #not found

    def post(self,surveyid):
        '''
        Creates a new report by it's surveyid.
        '''
        data = resources.parsers.ParseTestReports.parser.parse_args()
        #data = Report.parser.parse_args()

        if not check_fpq(data['f'], data['p'], data['q']):
            return {'message': "f,p and q must have values between 0.0 and 1.0"}, 400 #bad request

        report = ReportModel(surveyid, data['prr'], data['irr'], data['f'], data['p'], data['q'], json.dumps(data['answers']))
        try:
            report.save_to_db()
        except:
            return {'message': "error while inserting report"}, 500
        return report.tojson(), 201 # created


class ListReports(Resource):
    '''
    This ressource is for testing.
    '''
    def get(self):
        '''
        Return all reports stored on the client.
        ''' 
        return {'reports': [ x.tojson() for x in ReportModel.query.all()]}
