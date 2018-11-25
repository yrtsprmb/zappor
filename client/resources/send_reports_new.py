import json
import requests
from pprint import pprint
from flask_restful import Resource

from intern.config import serviceprovider_reports
from models.reports import ReportModel
# tests
#from tests.tests import data_report

# sends reports automatically to the server
#
# 1st: look all available survey ids in reports / oder: siehe ob treffer und nehme diesen, falls zeitlich
# 2nd: loop through all available surveys and do the following:
#       extrahiere die survey_id
#       bereite den rest der infos fuer ein report json format auf:
#       data landet dann hier: report = requests.post(serviceprovider_reports + surveyid, json=data_report)
#       ab die post
#
#
class SendReportNew(Resource):

    def get(self):

        reports = ReportModel.query.all()
        print('reports')                                #debug
        print(reports)                                  #debug
        print('------------------------------------')   #debug

        # loop through all reports
        for report in reports:
            report_serviceprovider = []
            print("Name of the surveyid: " + report.surveyid) #debug
            surveyid = report.surveyid

            report_serviceprovider.append({'prr': 1, 'irr': 1, 'f': report.f, 'p': report.p, 'q': report.q, 'answers': report.answers })
            print(report_serviceprovider[0])

            helga = report_serviceprovider[0]


            zepp = requests.post(serviceprovider_reports + surveyid, json=helga)
            code_response = zepp.status_code

            print(zepp.json()) #debug
            print(code_response) #debug

            # after the report was sended to the server, it should be deleted from the DB
            # TODO: delete all reports at once?
            report_to_delete = ReportModel.find_by_surveyid(surveyid)
            if report_to_delete is None:
                return {'message': "Error - report for surveyid '{}' does not exist anymore".format(surveyid)}, 400 #bad request

            try:
                report_to_delete.delete_from_db()
            except:
                return {'message': "error while deleting report"}, 500 #internal server error
            return report.tojson(), 201 # created



        return {'message': "test suceeded"}, 200 #ok
