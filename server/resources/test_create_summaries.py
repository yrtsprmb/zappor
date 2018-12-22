#resources/create_summaries.py

from flask_restful import Resource
from models.report import ReportModel
from models.survey import SurveyModel
#from models.summaries import SummaryModel

from internal.test_create_summaries import CreateSummaries


class Test(Resource):
    '''
    TODO: get with two values
    '''
    def get(self,surveyid):
        '''
        Return a summary of all qids belonging to a specific survey.
        Tooks all reports belonging to a surveyid/qid combination and generates a new summary per qid.
        If there exists already a summary for that qid, the old one will be overwritten.
        '''
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()

        report_answers = CreateSummaries.list_answers(reports)
        qids = CreateSummaries.extract_qids(report_answers)

        for qid in qids:
            CreateSummaries.create_summary(surveyid,qid)

        return {'message': 'fuck yeah' }, 200 #ok
