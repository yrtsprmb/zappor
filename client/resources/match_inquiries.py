import json
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel

from intern.matchings import generate_answers_by_surveyid, allmatchingsurveys, find_matches, client, server

class MatchInquiries(Resource):
    def get(self):


        #client = ClientInquiriesModel.query.all()
        #server = ServerInquiriesModel.query.all()
        #print(client)
        #print(server)

        # 1st: find all matches
        matches = find_matches(client,server)
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
            prr = 1
            irr = 1
            f = 0.66
            p = 0.77
            q = 0.88
            #3b) generate answers json.dumps(data['answers'])
            answers = generate_answers_by_surveyid(survey,matches)
            # save them to the db
            report = ReportModel(surveyid,prr,irr,f,p,q,json.dumps(answers))
            try:
                report.save_to_db()
            except:
                return {'message': "error while inserting report for surveyid'{}'. ".format(surveyid)}, 500
            return {'message': "reports sucessful matched and prepared"}, 202 #accepted
