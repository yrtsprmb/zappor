import json
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel

#from messenger import Messenger

class RequestSurvey(Resource):
    def get(self):
    # TODO: get the files from a request
        umfragen = {
            "surveys": [
                {
                    "surveyid": "surveyactive",
                    "serviceprovider": "radio_a",
                    "status": "active",
                    "questions": [
                        {
                            "qid": 1,
                            "name": "gender",
                            "type": "ordinal",
                            "options": [
                                "male",
                                "female",
                                "divers"
                            ]
                        },
                        {
                            "qid": 2,
                            "name": "family_status",
                            "type": "ordinal",
                            "options": [
                                "ledig",
                                "verheiratet",
                                "verwitwet",
                                "geschieden"
                            ]
                        }
                    ]
                },
                {
                    "surveyid": "surveypassive",
                    "serviceprovider": "radio_b",
                    "questions": [
                        {
                            "qid": 3,
                            "name": "gay",
                            "type": "ordinal",
                            "options": [
                                "yes",
                                "no",
                                "bi"
                            ]
                        },
                        {
                            "qid": 4,
                            "name": "favoritemusic",
                            "type": "ordinal",
                            "options": [
                                "jazz",
                                "negermusik",
                                "techno",
                                "hiphop"
                            ]
                        }
                    ]
                }

            ]
        }

        # takes a json in form of survey.json
        # and create out of the json the questions and save them to the database
        listevonsurveys = (umfragen['surveys'])
        for survey in listevonsurveys: #fuer jedes dictonairy in der liste
            #generate surveyids, serviceprovider for the questions format
            surveyid = (survey['surveyid'])
            serviceprovider = (survey['serviceprovider'])

            #generate qid, qname, qtype, qoptions for the questions format
            questions = (survey['questions'])
            for question in questions:
                qid = question['qid']
                name = question['name']
                type = question['type']
                options = question['options']

                print("surveyid: " + surveyid)                  #debug
                print("serviceprovider: " + serviceprovider)    #debug
                print("qid: " + str(qid))                       #debug
                print("qname: " + name)                        #debug
                print("qtype: " + type)                        #debug
                print("qoptions: " + json.dumps(options))      #debug
                print("____________________________")           #debug

                #tsave question to the db
                frage = ServerInquiriesModel(qid,surveyid,serviceprovider,name,type,json.dumps(options))
                frage.save_to_db()
