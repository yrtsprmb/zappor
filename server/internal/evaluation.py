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


def bins_per_qid(qid,list_of_report_objects):
    '''
    Determines quantity of bins per qid.
    TODO: exception einbauen.
    '''
    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

        for answer in answerlist: #loop throw dictionairis
            #bins = 0
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
    counter = 0

    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

        for answer in answerlist: #loop throw dictionairis
            if qid == answer['qid']:
                    histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
                    counter += 1
    return {'histogram': histogram_list, 'counts': counter }




def extract_from_reports(qid,list_of_report_objects):
    '''
    Returns the name and options to a qid for a specific report.
    '''
    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

        for answer in answerlist: #loop throw dictionairis
            if qid == answer['qid']:
                return {'name': answer['question'], 'options': answer['options']}
                # if f,p,q should implemented later, this could be done here.
                #return {'name': answer['question'], 'options': answer['options'],'f': answer['f'], 'p': answer['p'], 'q': answer['q']}
            else:
                pass #todo: catch error


def extract_from_surveys(qid,survey):
    '''
    Returns the name, type and options to a qid for a specific survey.
    '''
    questions = json.loads(survey.questions)
    for question in questions:
        if qid == question['qid']:
            print(question['type'])
            return { 'name': question['name'], 'type': question['type'], 'options': question['options']}
        else:
            pass #todo: catch error

################################################################################


def list_answers(list_of_report_objects):
    '''
    Returns a list of all given answers for a list of report objects.
    The answerlist is a list of list which contains dictionairis. [[{ }]]
    Not used.
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
    Not used.
    '''
    qids = []
    for answers in listofanswers:
        for answer in answers:
            qid = (answer['qid'])
            if qid not in qids:
                qids.append(qid)
    return qids


def counting_histogram_values_old(qid,list_of_report_objects):
    '''
    Counts values for histogram bins. Takes a qid and a list of report objects.
    Returns a histogram (list) with all summarized bins.
    '''
    bins = bins_per_qid(qid,list_of_report_objects)
    histogram_list = [0] * bins
    print("bins")
    print(bins)
    counter = 0

    for report in list_of_report_objects:
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

        for answer in answerlist: #loop throw dictionairis

            if qid == answer['qid']:
                    histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
                    counter = counter + 1
                    print(counter)
    return histogram_list

def extract_qid_info2(qid, list_of_report_objects):

    bins = bins_per_qid(qid,list_of_report_objects)
    histogram_list = [0] * bins
    print("bins")
    print(bins)

    for report in list_of_report_objects:
        print(report)
        answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
        for answer in answerlist: #loop throw dictionairis
            if qid == answer['qid']:
                    name = answer['name']
                    histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
    return histogram_list


def extract_qid_info(listofanswers):
    '''
    Takes a list of a list of dictionaires (all answers belonging to reports for a specific survey).
    Returns a list of dictinairis with qid, name
    '''
    questions = []
    qids = []
    qid = ""
    for answers in listofanswers:
        for answer in answers:
            print(answer)
            qid = (answer['qid'])
            name = (answer['question'])
            options = json.dumps((answer['options']))
            print("---------------------------------")
            print(qid)
            print(name)
            print(options)
            #print(type(answer['options']))
            print("---------------------------------")
            if qid not in qids:
                qids.append(qid)
                questions.append({'qid':qid, 'name': name})
    return questions




# def counting_histogram_values(qid,list_of_report_objects):
#     '''
#     Counts values for histogram bins. Takes a qid and a list of report objects.
#     Returns a histogram (list) with all summarized bins.
#     '''
#     bins = bins_per_qid(qid,list_of_report_objects)
#     histogram_list = [0] * bins
#     print("bins")
#     print(bins)
#
#     for report in list_of_report_objects:
#         answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
#         counter = 0
#         for answer in answerlist: #loop throw dictionairis
#             if qid == answer['qid']:
#                     histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
#                     counter += 1
#     return histogram_list





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
