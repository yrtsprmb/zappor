#resources/summaries.py

import json
from flask_restful import Resource, request

from models.summaries import SummaryModel
from models.survey import SurveyModel

import resources.parsers
from resources.parsers import check_if_bits

############################################
## Ressource for Summaries
############################################

class Summary(Resource):
    '''
    Internal REST resource:
    Returns all summaries belonging to a specific survey id.
    Returns a list with a summary of evaluated reports to an surveyid
    '''

    def get(self,surveyid):
        '''
        Internal REST resource:
        Returns all summaries belonging to a specific survey id.
        Returns a list with a summary of evaluated reports to an surveyid
        '''
        smry = [ x.tojson() for x in SummaryModel.query.filter_by(surveyid=surveyid)]
        if smry == []:
            return {'message': "no summary found for surveyid '{}' ".format(surveyid)}, 400
        return {'summary': smry }


    def post(self, surveyid):
        '''
        Server REST testing resource:
        Creates a summary for a specific survyid.
        This API is for testing the server functionality.
        '''
        data = resources.parsers.ParseSummariesPost.parser.parse_args()

        smmry = SummaryModel(data['qid'],
                                surveyid,
                                data['name'],
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answers']))
        try:
            smmry.save_to_db()
        except:
            return {'message': "Error while saving summary."}, 500 #internal server error
        return {'TEST API (no productive use)': smmry.tojson()}, 201 #created


    def delete(self,surveyid):
        '''
        Server REST testing resource:
        Deletes all summaries belonging to a surveyid.
        TODO: needs to be implemented
        '''
        # smmrys = SummaryModel.find_by_surveyid(surveyid)
        # print(smmrys)
        # if smmrys:
        #     try:
        #         smmrys.delete_from_db()
        #     except:
        #         return {'message': "Error while trying to delete the summaries."}, 500 #internal server error
        #
        #     return {'message': "Summaries belongig to surveyid '{}' deleted.".format(surveyid)}, 202 #accepted
        return {'message': " TEST API (no productive use)."}, 400 #bad request


class ListSummaries(Resource):
    def get(self):
        '''
        Server REST resource for testing:
        Returns a list with all summaries in the database.
        '''
        return {'summaries': [ x.tojson() for x in SummaryModel.query.all()]}, 200 #ok
