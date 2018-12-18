#resources/summaries.py
import json
from flask_restful import Resource, request

from models.summaries import SummaryModel
from models.survey import SurveyModel

#import resources.parsers
#from resources.parsers import check_fpq, check_if_bits

############################################
## Ressource for Summaries
############################################

class Summary(Resource):
    # returns a list with a summary of evaluated reports to an surveyid
    def get(self,surveyid):
        smry = [ x.tojson() for x in SummaryModel.query.filter_by(surveyid=surveyid)]
        if smry == []:
            return {'message': "no summary found for surveyid '{}' ".format(surveyid)}, 400
        return {'summary': smry }
        # {'reports': [ x.tojson() for x in ReportModel.query.filter_by(surveyid=surveyid)]}
