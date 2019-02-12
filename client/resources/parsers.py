# resources/parsers.py
from flask_restful import reqparse

##################################################################
## This file contains all parsers for the REST API
## as well as validation checks for incoming data.
##################################################################

class ParseClientInquiriesPost:
    '''
    Parser for client inquiries (POST requests).
    '''
    parser = reqparse.RequestParser()
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
    parser.add_argument('answer',
        type=int,
        action='append',
        required=False,
        help="answer is missing"
    )
    parser.add_argument('qdescription',
        type=str,
        required=False,
        help="qdescription is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=False,
        help="locked is missing"
    )
    parser.add_argument('f',
        type=float,
        required=False,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=False,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=False,
        help="q value is missing"
    )


class ParseClientInquiriesPut:
    '''
    Parser for client inquiries (PUT requests).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('answer',
    type=int,
    action='append',
    required=False,
    help="answer is missing"
    )
    parser.add_argument('qdescription',
        type=str,
        required=False,
        help="qdescription is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=True,
        help="locked is missing or not correct"
    )
    parser.add_argument('f',
        type=float,
        required=True,
        help="f is missing or not correct"
    )
    parser.add_argument('p',
        type=float,
        required=True,
        help="p is missing or not correct"
    )
    parser.add_argument('q',
        type=float,
        required=True,
        help="q is missing or not correct!"
    )


class ParseTestClientInquiries:
    '''
    Parser for client inquiries (for testing).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('type',
        type=str,
        required=False,
        help="type is missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=False,
        help="options are missing"
    )
    parser.add_argument('answer',
        type=int,
        action='append',
        required=False,
        help="answer is missing"
    )
    parser.add_argument('qdescription',
        type=str,
        required=False,
        help="qdescription is missing"
    )
    parser.add_argument('prr_answer',
        type=int,
        action='append',
        required=False,
        help="prr is missing"
    )
    parser.add_argument('irr_answer',
        type=int,
        action='append',
        required=False,
        help="irr is missing"
    )
    parser.add_argument('responded',
        type=bool,
        required=False,
        help="responded is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=False,
        help="locked is missing"
    )
    parser.add_argument('f',
        type=float,
        required=False,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=False,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=False,
        help="q value is missing"
    )


class ParseTestServerInquiries:
    '''
    Parser for server inquiries (for testing).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('qid',
        type=str,
        required=True,
        help="qid is missing"
    )
    parser.add_argument('surveyid',
        type=str,
        required=True,
        help="surveyid is missing"
    )
    parser.add_argument('serviceprovider',
        type=str,
        required=True,
        help="serviceprovider is missing"
    )
    parser.add_argument('type',
        type=str,
        required=True,
        help="type missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=True,
        help="options are missing"
    )
    parser.add_argument('qdescription',
        type=str,
        required=False,
        help="qdescription is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=True,
        help="locked missing"
    )
    parser.add_argument('quizmode',
        type=bool,
        required=True,
        help="quizmode missing"
    )


class ParseTestReports:
    '''
    Parser for reports (for testing).
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('prr',
        type=bool,
        required=True,
        help="prr value"
    )
    parser.add_argument('irr',
        type=bool,
        required=True,
        help="irr value"
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
        help="answer value is missing"
    )


class ParseConfiguration:
    '''
    TODO: Parser for configuration of the client.
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('global_f',
        type=float,
        required=True,
        help="global f is missing"
    )
    parser.add_argument('global_p',
        type=float,
        required=True,
        help="global p is missing"
    )
    parser.add_argument('global_q',
        type=float,
        required=True,
        help="global q missing"
    )
    parser.add_argument('dsgvo',
        type=bool,
        required=True,
        help="dsgvo"
    )
    parser.add_argument('quizmode',
        type=bool,
        required=True,
        help="quizmode"
        )

def check_bool(type,list):
    '''
    If a type is 'bool', the list 'options' must have a length of 2.
    And only one option can be set to 1.
    '''
    if not (type =='bool'):
        return True

    if (len(list) == 2) and (list == [0,1] or list == [1,0]):
            return True
    return False

def check_mc(type,list):
    '''
    If a type is 'mc', only 1 digit is allowed in the whole answer list.
    '''
    if (type == 'mc') and (list.count(1) != 1):
        return False
    return True

def check_fpq(f,p,q):
    '''
    Checks if f,p and q values are correct (between 0.0 and 1.0).
    '''
    return ((f <= 0.1 and f >= 0.0) and (p <= 1.0 and p >= 0.0) and (q <= 1.0 and q >= 0.0))

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
