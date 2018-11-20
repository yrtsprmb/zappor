from flask_restful import Resource, reqparse
from models.surveys import SurveyModel

class Survey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('longterm',
        type=bool,
        required=True,
        help="lvalue ongterm is missing"
    )
    parser.add_argument('done',
        type=bool,
        required=True,
        help="value done is missing"
    )

    def get(self,surveyid):
        survey = SurveyModel.find_by_surveyid(surveyid)
        if survey:
            return survey.tojson()
        return {'message': "Survey not found"}, 404 #not found

    #only for testing, surveys will be received by the server
    def post(self,surveyid):
        data = Survey.parser.parse_args()
        #write question only in db if it belongs unique to a surveyid
        if SurveyModel.find_by_surveyid(surveyid):
             return {'message': "surveyid '{}' already exist in database.".format(surveyid)}, 400 #bad request

        survey = SurveyModel(surveyid, data['longterm'], data['done'])
        try:
            survey.save_to_db()
        except:
            return {'message': "error while save survey data for '{}'. ".format(surveyid)}, 500
        return {'message': "survey '{}' stored in db. Please note, this is only for testing. ".format(surveyid)}, 500
        #return survey.tojson(), 201 # created

#shows all surveys
class ListSurveys(Resource):
    def get(self):
        return {'surveys in client-db': [ x.tojson() for x in SurveyModel.query.all()]}
