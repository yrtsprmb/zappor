# resources/parsers.py
from flask_restful import reqparse
from internal.helpers import Auxiliary
import json

##################################################################
## This file contains all parsers for the REST API
## as well as validation checks for incoming data.
##################################################################

class ParseUser:
    '''
    Parser for user.
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="problems with username"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="problems with the passowrd"
    )


class ParseSurveysPost:
    '''
    Parser for surveys (POST requests).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('serviceprovider',
        type=str,
        required=True,
        help="serviceprovider is missing"
    )
    parser.add_argument('status',
        type=str,
        required=True,
        help="status value is missing"
    )
    parser.add_argument('sdescription',
        type=str,
        required=True,
        help="sdescription is misssing"
    )
    parser.add_argument('questions',
         type=dict,
         action='append',
         required=True,
         help="error with questions"
    )


class ParseSurveysPut:
    '''
    Parser for surveys (put requests).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('status',
        type=str,
        required=True,
        help="status is missing or not correct"
    )


class ParseReportsPost:
    '''
    Parser for reports (POST requests).
    '''
    parser = reqparse.RequestParser()

    parser.add_argument('prr',
        type=bool,
        required=True,
        help="prr is missing"
    )
    parser.add_argument('irr',
        type=bool,
        required=True,
        help="irr is missing"
    )
    parser.add_argument('f',
        type=float,
        required=True,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=True,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=True,
        help="q value is missing"
    )
    parser.add_argument('answers',
        type=dict,
        action='append',
        required=True,
        help="answers are missing"
    )


class ParseSummariesPost:
    '''
    Parser for summaries (POST requests).
    '''
    parser = reqparse.RequestParser()

    parser.add_argument('qid',
        type=int,
        required=True,
        help="qid is missing"
    )
    parser.add_argument('name',
        type=str,
        required=True,
        help="name is missing"
    )
    parser.add_argument('type',
        type=str,
        required=True,
        help="type is missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=True,
        help="options are missing"
    )
    parser.add_argument('answers',
        type=int,
        action='append',
        required=True,
        help="answers are missing"
    )
    parser.add_argument('counter',
        type=int,
        required=True,
        help="counter is missing"
    )


def check_fpq(f,p,q):
    '''
    Checks if f,p and q values are correct (between 0.0 and 1.0).
    '''
    return ((f <= 1.0 and f >= 0.0) and (p <= 1.0 and p >= 0.0) and (q <= 1.0 and q >= 0.0))


def check_if_bits(list):
    '''
    Checks if the values of a an answerlist are either 1 or 0.
    '''
    for value in list:
        if(value !=0 and value !=1):
            return False
    return True


def check_type(status):
    '''
    Checks if the type of an inquiry is correct.
    Valid values are 'cbx' for checkbox, 'mc' for multiple choice and 'bool' for boolean.
    '''
    if(status != 'cbx' and status != 'mc' and status != 'bool'):
        return False
    return True

def check_bool(status):
    '''
    If a type is 'bool', the list 'options' must have a length of 2. TODO
    '''
    if(status != 'cbx' and status != 'mc' and status != 'bool'):
        return False
    return True


def check_status(status):
    '''
    Checks if the values of the status string of a survey is valid.
    Validity check for surveys.
    '''
    if(status != 'created' and status != 'active' and status != 'done'):
        return False
    return True


def correct_qids(report_list,survey_list):
    '''
    Checks if the qids in a report is also existing survey belonging to the report.
    Validity check for reports.
    '''
    for qid in report_list:
        if (qid not in survey_list):
            return False
    return True


def correct_bin_count(qid_list,report_list,survey_list):
    '''
    Checks if the amount of bins are correct / same size like the survey.
    Validity check for reports.
    '''
    bins_report = []
    bins_survey = []

    for qid in qid_list:
        for answer in report_list:
            if (qid == answer['qid']):
                bins_report.append({'qid': qid, 'bins': len(answer['options'])})

    for qid in qid_list:
        for question in survey_list:
            if (qid == question['qid']):
                bins_survey.append({'qid': qid, 'bins': len(question['options'])})

    for x in bins_report:
        qid = x['qid']
        bins = x['bins']
        for y in bins_survey:
            if qid == y['qid']:
                if(bins != y['bins']):
                    print("error: bin size not equal")
                    return False
    return True


def check_answerlist_bits(answerlist):
    '''
    Checks if the values of the answers of a report are either 1 or 0.
    Validity check for reports.
    '''
    for answer in answerlist:
        for bit in answer['options']:
            if(bit !=0 and bit !=1):
                print("wrong value: not 0 or 1:") #debug
                print(bit) #debug
                return False
    return True


def check_incoming_report(reportobject,surveyobject):
    '''
    Checks if the values of an incoming report are correct.
    Validity check for reports.
    '''
    questionlist = json.loads(surveyobject.questions)
    answerlist = json.loads(reportobject.answers)

    qids_survey = Auxiliary.get_qids(questionlist)
    qids_report = Auxiliary.get_qids(answerlist)

    # check if qids are correct.
    if not correct_qids(qids_report,qids_survey):
        print("wrong qids") #debug
        return False

    # check if binsize for answers are correct.
    if not correct_bin_count(qids_report,answerlist,questionlist):
        print("error in answerlist: wrong bin size") #debug
        return False

    # check if bit values int the answer are correct.
    if not check_answerlist_bits(answerlist):
        print("error in answerlist") #debug
        return False
    return True

def check_incoming_survey(questionlist):
    '''
    Checks values of a created survey.
    Check if the type is correct and when it is a 'bool' question, the options list should have a length of 2.
    Checks if every qid is unique.
    '''
    qid_list = []
    for question in questionlist:
        print(question)
        if not check_type(question['type']):
            print("Error: wrong value for 'type' ") #debug
            return False

        # if a type is 'bool', the length of options should be 2.
        if ((question['type'] == 'bool') and (len(question['options']) !=2)):
            print("Error: for a 'bool' questions are only 2 options allowed") #debug
            return False

        # every qid should be unique
        if question['qid'] in qid_list:
            print("Error: 'qid' not unique.") #debug
            return False
        else:
            qid_list.append(question['qid'])

    return True
