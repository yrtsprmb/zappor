import json
from flask_restful import Resource, reqparse
from models.reports import ReportModel

#this class is only for testing
class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('prr',
        type=bool,
        required=True,
        help="prr value"
    )
    parser.add_argument('irr',
        type=bool,
        required=True,
        help="irr value"
    )
    parser.add_argument('f',
        type=float,
        required=True,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=True,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=True,
        help="q value is missing"
    )
    parser.add_argument('answers',
        type=str,
        action='append',
        required=True,
        help="answer value is missing"
    )

    def get(self,surveyid):
        report = ReportModel.find_by_surveyid(surveyid)
        if report:
            return report.tojson()
        return {'message': "report not found"}, 404 #not found

    def post(self,surveyid):
        data = Report.parser.parse_args()
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
