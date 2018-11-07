import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel

class SendReport(Resource):

    def get(self):
        print("Test SendReport")

        server = 'http://127.0.0.1:5000/'
        surveyid = 'testsurvey'

        #data = {"price": 15.99,"store_id": 6}

        data = {
           "prr": True,
           "irr": True,
           "f": 0.5,
           "p": 0.75,
           "q": 0.5,
           "answers":
           [
              {
        	   "qid": 88888,
        	   "question": "gender",
               "options": [1,0,0],
        	   "f":  0.5,
        	   "p":  0.75,
        	   "q":  0.5
              },
              {
        	   "qid": 66,
               "question": "time",
               "options": [1,0,0],
        	   "f":  0.5,
        	   "p":  0.75,
        	   "q":  0.5
              },
              {
               "qid": 67,
               "question": "family_status",
               "options": [1,0,1,0],
        	   "f":  0.5,
        	   "p":  0.75,
        	   "q":  0.5
              },
              {
               "qid": 36,
               "question": "income",
               "options": [1,0,1,0]
              },
              {
               "qid": 589,
               "question":"own_station",
               "options:": True,
        	   "f":  0.5,
        	   "p":  0.75,
        	   "q":  0.5
              }
           ]
        }

        #report = requests.post("http://127.0.0.1:5000/reports/testsurvey", json=data)
        #report = requests.post("http://127.0.0.1:5000/reports/" + surveyid, data=data)
        report = requests.post(server + "reports/" + surveyid, json=data)

        code_response = report.status_code
        print(report.json()) #debug
        print(code_response)

        #print(report.text)
        return code_response
