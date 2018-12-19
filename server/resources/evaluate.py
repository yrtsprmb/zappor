#resources/evaluate.py

import json
from flask_restful import Resource
from models.report import ReportModel
from internal.evaluation import list_answers, extract_qids, bins_per_qid, list_qids_dict, counting_histvalues_per_qid, counting_histogram_values

class EvaluateSurvey(Resource):
    '''
    TODO: Should return an evaluation of a survey.
    Tooks all reports belonging to a survey id and extracts all qid
    For every qid a summary will be genereated by counting the answer lists.
    '''

    def get(self,surveyid):
        '''
        TODO: should return an evaluation of allreports belonging to a surveyidself.
        This
        '''

        #sum_values = [sum(pair) for pair in zip(horst, helga)]


        #generates a list of report objects to a specific survey id
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()
        #print("Report Models")
        #print(reports) #debug

        #generate a list of list answers, which contains dictionaries
        listofanswers = list_answers(reports) #works
        # print("listofanswers")
        # print(listofanswers) #debug
        # print(type(listofanswers))

        qids = extract_qids(listofanswers) #works
        print("qids")
        print(qids)


        histogram_qid34 = counting_histogram_values(34,reports)
        print("histogram_qid34")
        print(histogram_qid34)

        return {'message': " '{}' ".format(histogram_qid34)}, 200 #ok

        # TODO:
        # für alle qid pro survey die histogramme ermitteln und dann in die datenbank speichern
        # dabei noch erfassen wie oft diese qids gezählt wurden.

        # horst = bins_per_qid(34,reports)
        # print("horst")
        # print(horst)

        #list of all availalbe qids:
        #qidlist = list_qids(reports)
        #print(qidlist)

        #generate list of all qids in all reports per surveyid
        #dictionaires with qids and length of their questions
        #qid_dict = list_qids_dict(reports)
        #print(qid_dict) #debug

        # horst = counting_histogram_values(34,reports)
        # print(horst)

        # for entry in qid_dict:
        #     qid = entry['qid']
        #     options = entry['options']
        #     print(qid)
        #     print(options)
        #     print(counting_histvalues_per_qid(qid,options,reports))



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
