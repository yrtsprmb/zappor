import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from internal.config import serviceprovider_surveys

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

            #generate qid, qname, qtype, qoptions and qdescpritons for the questions format
            questions = (survey['questions'])

            for question in questions:
                qid = question['qid']
                name = question['name']
                qtype = question['type']
                options = question['options']
                qdescription = question['qdescription']

                #save question to the db, only if it is not already known by surveyid
                if ServerInquiriesModel.already_in_db(surveyid,name):
                    print("survey and matching inquiries already in DB")
                    continue
                else:
                    print("surveyid: " + surveyid)                  #debug
                    print("serviceprovider: " + serviceprovider)    #debug
                    print("qid: " + str(qid))                       #debug
                    print("qname: " + name)                         #debug
                    print("qtype: " + qtype)                        #debug
                    print("qoptions: " + json.dumps(options))       #debug
                    print("qdescription: " + qdescription)          #debug
                    print("____________________________")           #debug
                    frage = ServerInquiriesModel(qid,surveyid,serviceprovider,name,qtype,json.dumps(options),qdescription,False,False) #TODO: quizmode und locked derzeit nur voreingestellt
                    frage.save_to_db()
                    print("new survey with surveyid '{}' available and fetched from the server.".format(surveyid))
                    #return {'message': }, 201 #created

        return {'message': "done."}, 200 #ok
