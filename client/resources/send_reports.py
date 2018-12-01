import json
import requests
from pprint import pprint
from flask_restful import Resource

from intern.config import serviceprovider_reports
from models.reports import ReportModel
from models.server_inquiries import ServerInquiriesModel

from db import db #TODO: in model verlagern

#############################################################
# sends reports automatically to the server
# if a report was sent, it will be deletetd from the db
# with all belonging server_inquiries
#############################################################
class SendReport(Resource):

    def get(self):

        if ReportModel.query.first():
            report = ReportModel.query.first()
            print('report')                                     #debug
            print(report)                                       #debug
            print('------------------------------------')       #debug
            print("Name of the surveyid: " + report.surveyid)   #debug

            surveyid = report.surveyid
            report_serviceprovider = {'prr': 1, 'irr': 1, 'f': report.f, 'p': report.p, 'q': report.q, 'answers': json.loads(report.answers) }
            print(report_serviceprovider)      #debug

            # contact the server of the serviceprovider. send report if suceed
            try:
                r = requests.post(serviceprovider_reports + surveyid, json=report_serviceprovider)
                code_response = r.status_code
                print(r.json())         #debug
                print(code_response)    #debug
            except requests.exceptions.ConnectionError as e:
                print(e)    #debug
                return {'message': "server not available. no report was sent: {} ".format(e)}, 500 #ok

            # after the report was sent to the server, it should be deleted from the DB
            report_to_delete = ReportModel.find_by_surveyid(surveyid)
            if report_to_delete:
                try:
                    #report_to_delete.delete_from_db()
                    print('report deleted from db.') #debug
                except:
                   return {'message': "error while deleting report"}, 500 #internal server error

            # after the report was sent to the server, server_inquiries belonging to the survey id should be deleted from the DB
            server_inquiries_to_delete = ServerInquiriesModel.find_all_by_surveyid(surveyid)
            if server_inquiries_to_delete is None:
                return {'message': "no survey inquiries for surveyid '{}' to delete.".format(surveyid)}, 400 #bad request

            try:
                db.session.query(ServerInquiriesModel).filter(ServerInquiriesModel.surveyid==surveyid).delete()
                db.session.commit()
                print('server inquiries deleted') #debug

            except:
               return {'message': "error while deleting survey inquiries"}, 500 #internal server error
            #return report.tojson(), 200 #ok
            return {'message': "report to surveyid '{}' was sent to the serviceprovider.".format(surveyid)}, 200 #ok

        return {'message': "no reports to send."}, 200 #ok
