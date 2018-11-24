import json
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel

from intern.matchings import generate_answers_by_surveyid, find_matching_surveys, find_matches
from intern.config import global_f, global_p, global_q, global_irr, global_prr


# tooks all available inquiries from client and server and match them together
# positive matches are saved in the reports table
class MatchInquiries(Resource):
    def get(self):

        # {'inquiries': [ x.tojson() for x in ClientInquiriesModel.query.all()]}

        client = ClientInquiriesModel.query.all() # all client inquiries
        server = ServerInquiriesModel.query.all() # all server inquiries
        print('client inquiries')       #debug
        print(client)                   #debug
        print('server inquiries')       #debug
        print(server)                   #debug
        print("---------------------")  #debug

        # 1st: find all matches
        matches = find_matches(client,server)
        #matches = find_matches(client,servertest)

        print("matches")                #debug
        print(matches)                  #debug
        print("---------------------")  #debug

        # 2nd: identify all surveyids which have an match
        surveys = find_matching_surveys(matches)
        print("surveys which have matches matches") #debug
        print(surveys)                              #debug
        print("---------------------")              #debug

        # 3rd) generate answers by surveyid
        #for survey in surveys:
        #        print(generate_answers_by_surveyid(survey['surveyid'],matches))


        # 3) generate report data and save the reports to the database
        for survey in surveys:
            surveyid = survey
            prr = global_prr #TODO: nur global wenn, lokal nichts gesetzt
            irr = global_irr #TODO: nur global wenn, lokal nichts gesetzt
            f = global_f
            p = global_p
            q = global_q

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

        return {'message': "no new matches, all available matches already in reports"}, 200 #ok
