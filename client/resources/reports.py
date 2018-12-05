import json
from flask_restful import Resource
from models.reports import ReportModel
import resources.parsers
from resources.parsers import check_fpq, check_if_bits


##################################################################
## only for testing, reports are generated automatic internally
##################################################################
class Report(Resource):

    def get(self,surveyid):
        report = ReportModel.find_by_surveyid(surveyid)
        if report:
            return report.tojson()
        return {'message': "report not found"}, 404 #not found

    def post(self,surveyid):
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


#show all reports
class ListReports(Resource):
    def get(self):
        return {'reports': [ x.tojson() for x in ReportModel.query.all()]}
