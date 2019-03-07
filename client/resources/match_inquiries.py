#resources/match_inquiries
import json
from flask_restful import Resource
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel
from models.config import ConfigurationModel

from internal.matchings import generate_answers_by_surveyid, find_matching_surveys, find_matches



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
        # clinet inquiries which are not locked and answered by the user
        client = ClientInquiriesModel.query.filter_by(locked='0').filter_by(responded='1').all()
        cnfg = ConfigurationModel.find()

        # all server inquiries
        server = ServerInquiriesModel.query.all()
        # print('client inquiries')       #debug
        # print(client)                   #debug
        # print('server inquiries')       #debug
        # print(server)                   #debug
        # print("---------------------")  #debug

        # 1st: find all matches
        matches = find_matches(client,server)

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
            prr = 1 #deprecated, since every inquiry gets an PRR
            irr = 1 #for future usage: Basic RAPPOR mode.
            f = cnfg.global_f
            p = cnfg.global_p
            q = cnfg.global_q

            #3b) generate answers json.dumps(data['answers'])
            answers = generate_answers_by_surveyid(survey,matches)
            print("testanswers")
            print(answers)
            print(type(answers))

            # save them to the db
            report = ReportModel(surveyid,prr,irr,f,p,q,json.dumps(answers))

            if not ReportModel.find_report_by_surveyid(surveyid):
                try:
                    report.save_to_db()
                    return {'message': "report sucessful matched and saved to db"}, 202 #accepted
                except:
                    return {'message': "error while inserting report for surveyid'{}'. ".format(surveyid)}, 500 #internal server error

        return {'message': "no new matches."}, 200 #ok
