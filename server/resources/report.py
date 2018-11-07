import json
from flask_restful import Resource, reqparse, request

from models.report import ReportModel
from models.survey import SurveyModel

############################################
######## Ressources for reports
############################################

class Report(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument('surveyid',
    #    type=str,
    #    required=True,
    #    help="surveyid is missing"
    #)
    parser.add_argument('prr',
        type=bool,
        required=True,
        help="prr is missing"
    )
    parser.add_argument('irr',
        type=bool,
        required=True,
        help="irr is missing"
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
        type=dict,
        action='append',
        required=True,
        help="answers are missing"
    )

    # returns a list with all reports to a specific survey in the database
    def get(self,surveyid):
        return {'reports': [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]}

    # writes an report from the client to the db, only if the surveyid is known to the server
    #TODO: check if the input data is correct
    def post(self, surveyid):
        print("request: ", request.args)
        if SurveyModel.find_active_survey_by_id(surveyid):
            #data = request.get_json()
            data = Report.parser.parse_args()
            print(data)
            #print(data['answers'])
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


# Testing Resource: returns a list with all reports in the database
class ListReports(Resource):
    def get(self):
        return {'reports': [ x.tojson() for x in ReportModel.query.all()]}
