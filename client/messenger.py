import requests
import json
from pprint import pprint #only for testing

#set the addresses of a service provider
server = 'http://127.0.0.1:5000/'



## interface to Serviceprovider
##sends request to a surver for new surveys
##sends responses to a server in form of reports
class Messenger():
    # sends a get request to the service provider to lookup new surveys
    def ask_for_survey(server):
        surveys = requests.get(server + "surveyavailable")
        statuscode = surveys.status_code

        print(surveys.text) #debug
        #pprint(statuscode) #debug
        return print(statuscode)


    # sends a post request to the service provider
    def send_report(server,surveyid,data):
        report = requests.post(server + "report/" + surveyid, json=data)
        print(report.text)
        statuscode = report.status_code
        print(statuscode)
        #pprint(report.json()) #debug
        #pprint(statuscode) #debug
        return statuscode


Messenger.ask_for_survey(server)


###########################################
############# Tests #######################
###########################################


data = {
   "prr": True,
   "irr": True,
   "f": 0.5,
   "p": 0.75,
   "q": 0.5,
   "answers":
   [
      {
		 "qid": 1,
		 "question": "geilo",
         "data": [1,0,0]
      },
      {
		 "qid": 2,
		 "question": "geilstens",
         "data": 26
      },
      {
		 "qid": 3,
		 "question": "income",
         "data": [1,0,0]
      }

   ]
}

Messenger.send_report(server,"testsurvey",data)


## tests
