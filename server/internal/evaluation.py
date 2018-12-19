#internal/evaluation.py

import json
#from flask_restful import Resource, request
#from models.report import ReportModel
"""
Helping functions for the evaluation of surveys.

fur alle reports in der liste
gehe jeweils durch die antworten:
fur jede qid addiere die antworten in der liste auf.
"""

def list_answers(list_of_report_objects):
    '''
    Returns a list of all given answers for a list of report objects.
    The answerlist is a list of list which contains dictionairis. [[{ }]]
    '''
    answerlist = []
    for report in list_of_report_objects:
        answers = (json.loads(report.answers)) #make string to a list of dictionairis
        answerlist.append(answers)
    return answerlist


def extract_qids(listofanswers):
    '''
    Takes a list of a list of dictionaires (all answers belonging to reports for a specific survey).
    Returns a list of all qids which are in this input list.
    '''
    qids = []
    for answers in listofanswers:
        for answer in answers:
            qid = (answer['qid'])
            if qid not in qids:
                qids.append(qid)
    return qids

def bins_per_qid(qid,list_of_report_objects):
    '''
    Determines quantity of bins per qid.
    TODO: exception einbauen.
    '''
    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        for answer in answerlist: #loop throw dictionairis
            if qid == answer['qid']:
                bins = len(answer['options'])
    return bins


def counting_histogram_values(qid,list_of_report_objects):
    '''
    Counts values for histogram bins. Takes a qid and a list of report objects.
    Returns a histogram (list) with all summarized bins.
    '''
    bins = bins_per_qid(qid,list_of_report_objects)
    histogram_list = [0] * bins
    print("bins")
    print(bins)

    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        for answer in answerlist: #loop throw dictionairis
            if qid == answer['qid']:
                    histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
    return histogram_list




def list_qids_dict(list_of_report_objects):
    '''
    returns a list of dictionairis with the qid and the length of options
    TODO: function still needed?
    '''
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



def counting_histvalues_per_qid(qid,number_of_options,answerlist):
    '''
    TODO
    '''
    histogram_list = [0] * number_of_options #length of options list
    print("debug")
    print(type(qid))

    for answer in answerlist:
        if qid == int(answer['qid']):
            print("geilo")
            histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
    return(histogram_list)
