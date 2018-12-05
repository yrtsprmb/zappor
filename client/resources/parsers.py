# resources/parsers.py

from flask_restful import reqparse

##################################################################
## in this file are all parsers for the REST API
##################################################################

# parser for POST client inquiries
class ParseClientInquiriesPost:
    parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #     type=str,
    #     required=False,
    #     help="name error through parsing"
    # )
    parser.add_argument('type',
        type=str,
        required=True,
        help="liste is missing"
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


# parser for PUT client inquiries
class ParseClientInquiriesPut:
    parser = reqparse.RequestParser()
    parser.add_argument('answer',
    type=int,
    action='append',
    required=False,
    help="answer is missing"
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


# parser for testing the REST API
class ParseTestClientInquiries:
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


class ParseClientConf:
    parser = reqparse.RequestParser()

    parser.add_argument('serveraddress',
        type=str,
        required=True,
        help="server address is missing"
    )
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
    parser.add_argument('slider',
        type=float,
        required=True,
        help="global slider"
    )


class CheckRestInputValues:
    pass

# checks if f,p,q are float between 0 and 1
def check_fpq(f,p,q):
    return ((f <= 1.0 and f >= 0.0) and (p <= 1.0 and p >= 0.0) and (q <= 1.0 and q >= 0.0))

def check_if_bits(list):
    for value in list:
        if(value !=0 and value !=1):
            return False
    return True
