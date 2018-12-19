# resources/parsers.py

from flask_restful import reqparse

##################################################################
# in this file are all parsers for the REST API
# and also validation checks for values
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
    Parser for surveys (post requests).
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
    Parser for reports (post requests).
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
    Parser for summaries (post requests).
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
        required=False,
        help="answers are missing"
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


def check_status(status):
    '''
    Checks if the values of the status string is valid.
    '''
    if(status != 'created' and status != 'active' and status != 'done'):
        return False
    return True
