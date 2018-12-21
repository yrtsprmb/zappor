#resources/generate_summaries.py

import json
from flask_restful import Resource
from models.report import ReportModel
from models.survey import SurveyModel
from models.summaries import SummaryModel
from internal.evaluation import counting_histogram_values, extract_from_surveys, extract_from_reports


class GenerateSummaries(Resource):
    '''
    TODO: Should return a summary of a qid belonging to a specific survey.
    Tooks all reports belonging to a surveyid / qid combination and generates a new summary.
    If there exists already a summary, the old one will be overwritten.
    '''

    def get(self,surveyid):
        '''
        TODO: should return an evaluation of allreports belonging to a surveyidself.
        Deal with qid and type of qid!!!
        This
        '''

        qid = 62

        #first: check if survey exists.
        survey = SurveyModel.find_survey_by_id(surveyid)
        #print(survey)
        if survey == None:
            return {'message': " Cannot generate summery. Surveyid '{}' does not exist".format(surveyid)}, 400 #bad request

        #second: generate a list of report objects to a specific survey id
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()

        #third: count histogram and determine counts
        evaluation = counting_histogram_values(qid,reports)
        summed_answers = (evaluation['histogram'])
        count_answers = (evaluation['counts'])


        #fourth: determine other values for generating a summary:
        infos_from_reports = extract_from_reports(qid,reports)
        report_name = infos_from_reports['name']
        report_options = infos_from_reports['options']

        infos_from_survey = extract_from_surveys(qid,survey)
        survey_name = infos_from_survey['name']
        survey_type = infos_from_survey['type']
        survey_options = infos_from_survey['options']


        #fifth: if a prior summary already exists delete it, before writing the new one.
        old_smmry = SummaryModel.find_unique_summary(surveyid,qid)

        if old_smmry:
            #print("old_smmry deleted")
            #print(old_smmry)
            old_smmry.delete_from_db()

        #6th: write the new summary:

        smmry = SummaryModel(qid,surveyid,report_name,survey_type,json.dumps(survey_options),json.dumps(summed_answers))

        try:
            smmry.save_to_db()
        except:
            return {'message': "Error while saving summary."}, 500 #internal server error

        return {'message': " summary for qid 62 and report '{}' is sucessfully created.".format(surveyid)}, 200 #ok
