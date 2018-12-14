#internal/evaluate_reports.py

import json
#from flask_restful import Resource, request
#from models.report import ReportModel
"""
fur alle reports in der liste
gehe jeweils durch die antworten:
fur jede qid addiere die antworten in der liste auf.

"""


# returns a list of dictionairis with the qid and the length of options
def list_qids_dict(list_of_report_objects):
    qids = []
    qdict = []

    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        for answer in answerlist: #loop throw dictionairis
            qid = answer['qid']
            options = len(answer['options'])
            if qid not in qids:
                qids.append(qid)
                qdict.append({'qid': qid, 'options': options})
    return(qdict)

#d returns a list of all given answers for reports
def list_answers(list_of_report_objects):
    answerlist = []
    for report in list_of_report_objects:
        answers = (json.loads(report.answers)) #make string to a list of dictionairis
        answerlist.append(answers)
    return answerlist



# returns a list of answers belonging to a specific qid
def answers_per_qid(qid,answerlist):
    for answer in answerlist:
        if qid == answer['qid']:
            print("zepp")
    pass


def counting_histvalues_per_qid(qid,options,answerlist):
    histogram_list = [0] * options #length of list

    for answer in answerlist:
        if qid == answer['qid']:
            histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
    return(histogram_list)


def counting_histogram_values(qid,list_of_report_objects):
    finalsums = [0,0,0,0]
    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        for answer in answerlist: #loop throw dictionairis
            options = answer['options']

            if qid == answer['qid']:
                    finalsums = [sum(pair) for pair in zip(finalsums, answer['options'])]
                    #print(finalsums)
        #print("endergebnis")
        #print(finalsums)
    return(finalsums)



horst = [1,0,1,0,1,0,1]
helga = [1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]

[1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]
[1,0,1,0,1,0,1]

[1,0,1,0,1,0,1]



#sum_values = [sum(pair) for pair in zip(horst, helga)]
#print(sum_values)
