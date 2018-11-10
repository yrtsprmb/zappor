import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel

class RequestSurvey(Resource):

    def get(self):
        ## TODO: server variable auslagern.
        # request surveys from the server
        server = 'http://127.0.0.1:5000/'
        r = requests.get(server + "availablesurveys")
        umfragen = r.json()
        listevonsurveys = (umfragen['surveys'])

        # creates questions and save the to the db
        for survey in listevonsurveys: #fuer jedes dictonairy in der liste

            #generate surveyids, serviceprovider for the questions format
            surveyid = (survey['surveyid'])
            serviceprovider = (survey['serviceprovider'])

            #generate qid, qname, qtype, qoptions for the questions format
            questions = (survey['questions'])

            for question in questions:
                qid = question['qid']
                name = question['name']
                qtype = question['type']
                options = question['options']

                #save question to the db, only if it is not already known by surveyid
                if ServerInquiriesModel.schon_in_db(surveyid,name):
                    print("survey and matching inquiries already in DB")
                else:
                    print("surveyid: " + surveyid)                  #debug
                    print("serviceprovider: " + serviceprovider)    #debug
                    print("qid: " + str(qid))                       #debug
                    print("qname: " + name)                         #debug
                    print("qtype: " + qtype)                        #debug
                    print("qoptions: " + json.dumps(options))       #debug
                    print("____________________________")           #debug
                    frage = ServerInquiriesModel(qid,surveyid,serviceprovider,name,qtype,json.dumps(options))
                    frage.save_to_db()
