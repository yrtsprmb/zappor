import json
from flask_restful import Resource
from models.reports import ReportModel
import resources.parsers


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
