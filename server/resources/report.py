import sqlite3
from flask_restful import Resource, reqparse

from models.report import ReportModel

############################################
######## ressourcen for reports
############################################


class Report(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('surveyid',
        type=str,
        required=True,
        help="surveyid is missing"
    )
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
        type=str,
        required=True,
        help="answers are missing"
    )

    # writes an report from the client to the db
    def post(self, surveyid):
        # TODO: check if surveyid is in db: if not, ignore report

        data = Report.parser.parse_args()
        report = ReportModel(surveyid,
            data['prr'],
            data['irr'],
            data['f'],
            data['p'],
            data['q'],
            data['answers']
        )

        #try:
        report.insert()
        #except:
        #    return {'message': "error while inserting report with surveyid '{}'. ".format(surveyid)}, 500

        return report.json(), 201 # status CREATED
