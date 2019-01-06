#resources/request_surveys

import json
import requests
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from internal.config import serviceprovider_surveys, quizmode_config, locked_config, quizmode_config, configfile_f, configfile_p, configfile_q
from resources.parsers import check_type


class RequestSurvey(Resource):
    '''
    Request new surveys from the server and store them into the client database.
    '''
    def get(self):
        '''
        Request new surveys from the server. If the data is valid, the surveys are stored into the
        server inquiries table. If quizmode is activated, they will be also saved in the client inquiries table.
        '''
        # contact the server of the serviceprovider. get surveys if suceed
        try:
            r = requests.get(serviceprovider_surveys)
            umfragen = r.json()
            listevonsurveys = (umfragen['surveys'])
        except requests.exceptions.ConnectionError as e:
            print(e)    #debug
            return {'message': "server not available. no survey was requested: {} ".format(e)}, 500 #ok

        if quizmode_config is True:
            print("helga hat titten")
            #creates client inquiries:
            for survey in listevonsurveys:
                inquiries = (survey['questions']) #fuer jedes dictonairy in der liste
                print(inquiries)
                for inq in inquiries:
                    name = inq['name']
                    qtype = inq['type']
                    options = inq['options']
                    options_count = len(inq['options'])
                    answer = [0]* options_count
                    prr_answer = [0]* options_count
                    irr_answer = [0]* options_count
                    qdescription = inq['description']
                    responded = False
                    locked = locked_config
                    f = configfile_f
                    p = configfile_p
                    q = configfile_q

                    if ClientInquiriesModel.find_by_name(name):
                        print("client inquiry with name " + name + "already in db" ) #debug
                        continue
                    else:
                        if check_type(qtype):
                            inquiry = ClientInquiriesModel(name,qtype,json.dumps(options),json.dumps(answer),json.dumps(prr_answer),json.dumps(irr_answer),qdescription,responded,locked,f,p,q)
                            inquiry.save_to_db()
                            print("quizmode on: new inquiry with name '{}' saved to client inquiry.".format(name))
                        print("error: Type '{}' not correct.".format(qtype))

        # creates questions and save the to the db
        for survey in listevonsurveys: #for every dictonairy in a list of dictionairies
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
                qdescription = question['description']

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
                    if check_type(qtype):
                        frage = ServerInquiriesModel(qid,surveyid,serviceprovider,name,qtype,json.dumps(options),qdescription,quizmode_config,quizmode_config)
                        frage.save_to_db()
                        print("new survey with surveyid '{}' available and fetched from the server.".format(surveyid))
                    print("error: Type '{}' not correct.".format(qtype))

        return {'message': "done."}, 200 #ok
