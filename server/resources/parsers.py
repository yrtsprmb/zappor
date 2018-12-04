# resources/parsers.py

from flask_restful import reqparse

##################################################################
## in this file are all parsers for the REST API
##################################################################


class ParseUser:
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="probleme mit dem usernamen"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="probleme mit dem passwort"
    )


# parser for POST surveys
class ParseSurveysPost:
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
    parser.add_argument('comment',
        type=str,
        required=True,
        help="no comment"
    )
    parser.add_argument('questions',
         type=dict,
         action='append',
         required=True,
         help="error with questions"
    )


# parser for Put surveys
class ParseSurveysPut:
    parser = reqparse.RequestParser()
    parser.add_argument('status',
        type=str,
        required=True,
        help="status is missing or not correct"
    )


# parser for POST reports
class ParseReportsPost:
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

# checks if f,p,q are float between 0 and 1
def check_fpq(f,p,q):
    return ((f <= 1.0 and f >= 0.0) and (p <= 1.0 and p >= 0.0) and (q <= 1.0 and q >= 0.0))
