import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from intern.config import serviceprovider_reports
# tests
from tests.tests import data_report

class SendReport(Resource):

    def get(self):
        print("SendReport") # debug
        surveyid = 'test'

        report = requests.post(serviceprovider_reports + surveyid, json=data_report)
        code_response = report.status_code

        print(report.json()) #debug
        print(code_response) #debug

        return code_response
