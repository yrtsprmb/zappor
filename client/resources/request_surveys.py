import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from intern.config import serviceprovider_surveys

#############################################################
# requests surveys from the serviceprovider and store them
# as server inquiries in the db
#surveys -> server inquiries
#############################################################
class RequestSurvey(Resource):

    def get(self):
        # contact the server of the serviceprovider. get surveys if suceed
        try:
            r = requests.get(serviceprovider_surveys)
            umfragen = r.json()
            listevonsurveys = (umfragen['surveys'])
        except requests.exceptions.ConnectionError as e:
            print(e)    #debug
            return {'message': "server not available. no survey was requested: {} ".format(e)}, 500 #ok

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
                if ServerInquiriesModel.already_in_db(surveyid,name):
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
                    #return frage.tojson(), 201 #created
                    return {'message': "new survey with surveyid '{}' available and fetched from the server.".format(surveyid)}, 201 #created

        return {'message': "no new surveys available."}, 200 #ok
