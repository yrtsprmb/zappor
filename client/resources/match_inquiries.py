import json
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel

from intern.matchings import generate_answers_by_surveyid, allmatchingsurveys, find_matches
from intern.config import global_f, global_p, global_q, global_irr, global_prr

#tests
from intern.test_matching import clienttest, servertest

class MatchInquiries(Resource):
    def get(self):


        client = ClientInquiriesModel.query.all()
        server = ServerInquiriesModel.query.all()
        #print(client) #debug
        #print(server) #debug

        # 1st: find all matches
        #matches = find_matches(client,server)
        matches = find_matches(clienttest,servertest)
        #print("---------------------")
        #print("matches")
        #print(matches)

        # 2nd: identify all surveyids which have an match
        surveys = allmatchingsurveys(matches)
        #print("---------------------")
        #print("surveys which have matches matches")
        #print(surveys)

        # 3d) generate answers by surveyid
        #for survey in surveys:
        #        print(generate_answers_by_surveyid(survey['surveyid'],matches))
        print("---------------------")

        # 3) generate report data and save the reports to the database
        for survey in surveys:
            surveyid = survey
            prr = global_prr
            irr = global_irr
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
                    return {'message': "error while inserting report for surveyid'{}'. ".format(surveyid)}, 500
        return {'message': " surveyids already known in reports table"}, 200
