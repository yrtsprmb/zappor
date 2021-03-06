#resources/send_reports.py
import json
import requests
from pprint import pprint
from flask_restful import Resource

from internal.config import serviceprovider_reports, config_quizmode
from models.reports import ReportModel
from models.server_inquiries import ServerInquiriesModel
from models.archive import ArchiveModel
from models.config import ConfigurationModel
from datetime import datetime


class SendReport(Resource):
    '''
    This resource is responsible for sending reports to the server.
    If a report was sent, it will be deleted from the db with all belonging server_inquiries.
    '''
    def get(self):
        '''
        Sends a report to the server. After the report was sent, it deletes the report from the client and server inquiries belonging to them.
        '''
        cnfg = ConfigurationModel.find()
        if cnfg is None or cnfg.dsgvo != 1:
            return {'message': "Can't send reports with GDPR/DSGVO consent."}, 400 #bad request

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

            # a archive entry is made, for not answering surveys twice.
            report_to_delete = ReportModel.find_by_surveyid(surveyid)
            #new
            rchv = ArchiveModel.find_by_surveyid(surveyid)
            rchv.processed = True
            rchv.exit = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

            # after the report was sent to the server, it should be deleted from the DB
            if report_to_delete:
                try:
                    ServerInquiriesModel.delete_all_inqs_by_surveyid(surveyid)
                    report_to_delete.delete_from_db()
                    rchv.save_to_db()

                    if config_quizmode: #TODO: delete also all client inquries.
                        #ClientInquiriesModel.delete_all_client_inquiries()
                        pass
                    print('report and all server inquiries belonging to the report deleted from db.') #debug
                except:
                   return {'message': "error while deleting report"}, 500 #internal server error

            return {'message': "report to surveyid '{}' was sent to the serviceprovider.".format(surveyid)}, 200 #ok

        return {'message': "no reports to send."}, 200 #ok
