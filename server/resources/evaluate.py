#resources/evaluate.py

import json
from flask_restful import Resource
from models.report import ReportModel
from internal.evaluation import list_qids_dict, list_answers, counting_histvalues_per_qid, counting_histogram_values

class EvaluateReport(Resource):

    def get(self,surveyid):
        '''
        TODO: should return an evaluation of reports by surveyid
        '''

        #sum_values = [sum(pair) for pair in zip(horst, helga)]


        #generate list of report objects to specific survey id
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()
        # print(reports) #debug

        #generate a list of all answers
        answerlist = list_answers(reports)
        #print(answerlist) #debug
        #print(type(answerlist))

        #generate list of all qids in all reports per surveyid
        #dictionaires with qids and length of their questions
        qid_dict = list_qids_dict(reports)
        #print(qid_dict) #debug

        horst = counting_histogram_values(34,reports)
        print(horst)

        for entry in qid_dict:
            qid = entry['qid']
            options = entry['options']
            print(qid)
            print(options)
            print(counting_histvalues_per_qid(qid,options,reports))
        #
        #
        # #test = counting_histvalues_per_qid(qid_dict,answerlist)
        # #print(test)
        #
        # return {'message': " '{}' ".format(qid_dict)}, 200 #ok
        #takes answerlist and qdicts and generates the histogram_list
        #for entry in qid_dict:

        #generate answerlists:
        # for report in reports:
        #     answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        #     for answer in answerlist: #loop throw dictionairis
        #         print("antworten")
        #         print(answer)


        #print(qid_dict)

        #finalsums = qids['len_q']

        #helga = counting_histvalues_per_qid()


        # for qid in qid_dict:
        #     histogram_list = [0] * qid['options']
        #     for report in reports:
        #         pass


        #counting_list =
        #fur jede qid:
        #gehe durch alle reports und nehme das array
        # finalsums = [0,0,0,0]
        # for report in reports:
        #     answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        #     for answer in answerlist: #loop throw dictionairis
        #         options = answer['options']
        #         #hier den addierscheiß?
        #         #print(options)
        #         qid = 34 #test
        #
        #         if qid == answer['qid']:
        #
        #             #print(options)
        #             finalsums = [sum(pair) for pair in zip(finalsums, answer['options'])]
        #             print(finalsums)
        # print("endergebnis")
        # print(finalsums)



        #print("list qids") #debug
        #print(qids) #debug


        return {'message': " '{}' ".format(qid_dict)}, 200 #ok
