#resources/summaries.py

import json
from flask_restful import Resource, request

from models.report import ReportModel
from models.summaries import SummaryModel
from models.survey import SurveyModel

import resources.parsers
from resources.parsers import check_if_bits
from internal.summaries import SummaryHelper


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
        smrys = [ x.tojson() for x in SummaryModel.query.filter_by(surveyid=surveyid)]
        if smrys == []:
            return {'message': "no summary found for surveyid '{}' ".format(surveyid)}, 400
        return {'summaries': smrys }

    def post(self, surveyid):
        '''
        Server REST testing resource:
        Creates a summary for a specific survyid.
        This API is only for testing the server functionality.
        '''
        data = resources.parsers.ParseSummariesPost.parser.parse_args()

        smmry = SummaryModel(data['qid'],
                                surveyid,
                                data['name'],
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answers']),
                                data['counter'])
        try:
            smmry.save_to_db()
        except:
            return {'message': "Error while saving summary."}, 500 #internal server error
        return {'TEST API (no productive use)': smmry.tojson()}, 201 #created

    def delete(self,surveyid):
        '''
        Server REST testing resource:
        Deletes all summaries belonging to a specific surveyid.
        '''
        smmrys = SummaryModel.find_by_surveyid(surveyid)
        for smmry in smmrys:
            try:
                smmry.delete_from_db()
            except:
                return {'message': "Error while trying to delete summary."}, 500 #internal server error

        return {'TEST API (no productive use)': "Summaries belongig to surveyid '{}' deleted.".format(surveyid)}, 202 #accepted


class ListSummaries(Resource):
    def get(self):
        '''
        Server REST resource for testing:
        Returns a list with all summaries in the database.
        '''
        return {'summaries': [ x.tojson() for x in SummaryModel.query.all()]}, 200 #ok


class CreateSummaries(Resource):
    '''
    Creates for all reports to a surveyid new summaries.
    '''
    def get(self,surveyid):
        '''
        Return a summary of all qids belonging to a specific survey.
        Tooks all reports belonging to a surveyid/qid combination and generates a new summary per qid.
        If there exists already a summary for that qid, the old one will be overwritten.
        '''
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()

        report_answers = SummaryHelper.list_answers(reports)
        qids = SummaryHelper.extract_qids(report_answers)

        smmrs_per_survey = []
        for qid in qids:
            smmry = SummaryHelper.create_summary(surveyid,qid)

            smmrs_per_survey.append(smmry.tojson())

        return {'summaries': smmrs_per_survey }, 200 #ok
