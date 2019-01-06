#resources/match_inquiries

import json
from flask_restful import Resource
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel

from internal.matchings import generate_answers_by_surveyid, find_matching_surveys, find_matches
from internal.config import configfile_f, configfile_p, configfile_q


class MatchInquiries(Resource):
    '''
    Takes all available inquiries from client and server and match them together.
    Positive matches are saved in the reports table
    '''
    def get(self):
        '''
        The get request fetches all client inquiries which are not locked and answered by the use
        If they match in name, type and length of options they will be stored in reports belonging to a specific survey id.
        '''
        # only inquiries which are not locked and answered by the user
        client = ClientInquiriesModel.query.filter_by(locked='0').filter_by(responded='1').all()
        #client = ClientInquiriesModel.query.filter_by(locked='0').all() # only inquiries which are not locked by the user
        server = ServerInquiriesModel.query.all() # all server inquiries
        print('client inquiries')       #debug
        print(client)                   #debug
        # print('server inquiries')       #debug
        # print(server)                   #debug
        # print("---------------------")  #debug

        # 1st: find all matches
        matches = find_matches(client,server)
        #matches = find_matches(client,servertest)

        # print("matches")                #debug
        # print(matches)                  #debug
        # print("---------------------")  #debug

        # 2nd: identify all surveyids which have an match
        surveys = find_matching_surveys(matches)
        # print("surveys which have matches matches") #debug
        # print(surveys)                              #debug
        # print("---------------------")              #debug

        # 3) generate report data and save the reports to the database
        for survey in surveys:
            surveyid = survey
            prr = 1 #deprecated
            irr = 1 #deprecated
            f = configfile_f
            p = configfile_p
            q = configfile_q

            #3b) generate answers json.dumps(data['answers'])
            answers = generate_answers_by_surveyid(survey,matches)
            # save them to the db
            report = ReportModel(surveyid,prr,irr,f,p,q,json.dumps(answers))

            if not ReportModel.find_report_by_surveyid(surveyid):
                try:
                    report.save_to_db()
                    return {'message': "report sucessful matched and saved to db"}, 202 #accepted
                except:
                    return {'message': "error while inserting report for surveyid'{}'. ".format(surveyid)}, 500 #internal server error

        return {'message': "no new matches."}, 200 #ok
