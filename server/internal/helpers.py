#internal/helpers.py

import json
from models.report import ReportModel
from models.survey import SurveyModel
from models.summaries import SummaryModel


class Auxiliary:
    '''
    Contains helper functions.
    '''
    def get_qids(answers):
        '''
        Takes a list of dictionaires (all answers belonging to reports for a specific survey).
        Returns a list of all qids which are in this input list.
        '''
        qids = []
        for answer in answers:
            qid = (answer['qid'])
            if qid not in qids:
                qids.append(qid)
        return qids

    def extract_from_reports(qid,list_of_report_objects):
        '''
        Returns the name and options to a qid for a specific report.
        '''
        for report in list_of_report_objects:
            answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

            for answer in answerlist: #loop throw dictionairis
                if qid == answer['qid']:
                    return {'name': answer['question'], 'options': answer['options']}
                    # if f,p,q should implemented later, this could be done here.
                    #return {'name': answer['question'], 'options': answer['options'],'f': answer['f'], 'p': answer['p'], 'q': answer['q']}
                else:
                    pass #todo: catch error


    def extract_from_surveys(qid,survey):
        '''
        Returns the name, type and options to a qid for a specific survey.
        '''
        questions = json.loads(survey.questions)
        for question in questions:
            if qid == question['qid']:
                print(question['type'])
                return { 'name': question['name'], 'type': question['type'], 'options': question['options']}


    def bins_per_qid(qid,list_of_report_objects):
        '''
        Determines quantity of bins per qid.
        TODO: exception einbauen.
        '''
        for report in list_of_report_objects:
            answerlist = (json.loads(report.answers)) #make string to a list of dictionairis
            print('answerlist', answerlist)
            for answer in answerlist: #loop throw dictionairis
                print(answer)
                if qid == answer['qid']:
                    bins = len(answer['options'])
        return bins

    def extract_qids(listofanswers):
        '''
        Takes a list of a list of dictionaires (all answers belonging to reports for a specific survey).
        Returns a list of all qids which are in this input list.
        Not used.
        '''
        qids = []
        for answers in listofanswers:
            for answer in answers:
                qid = (answer['qid'])
                if qid not in qids:
                    qids.append(qid)
        return qids

    def list_answers(list_of_report_objects):
        '''
        Returns a list of all given answers for a list of report objects.
        The answerlist is a list of list which contains dictionairis. [[{ }]]
        Not used.
        '''
        answerlist = []
        for report in list_of_report_objects:
            answers = (json.loads(report.answers)) #make string to a list of dictionairis
            answerlist.append(answers)
        return answerlist

    def counting_histogram_values(qid,list_of_report_objects):
        '''
        Counts values for histogram bins. Takes a qid and a list of report objects.
        Returns a histogram (list) with all summarized bins.
        '''
        bins = Auxiliary.bins_per_qid(qid,list_of_report_objects)
        histogram_list = [0] * bins
        print("bins")
        print(bins)
        counter = 0

        for report in list_of_report_objects:
            answerlist = (json.loads(report.answers)) #make string to a list of dictionairis

            for answer in answerlist: #loop throw dictionairis
                if qid == answer['qid']:
                        histogram_list = [sum(pair) for pair in zip(histogram_list, answer['options'])]
                        counter += 1
        return {'histogram': histogram_list, 'counts': counter }

    def create_summary(surveyid,qid):
        '''
        Return a summary of a qid belonging to a specific survey.
        Tooks all reports belonging to a surveyid/qid combination and generates a new summary.
        If there exists already a summary for that qid, the old one will be overwritten.
        '''
        #first: check if survey exists.
        survey = SurveyModel.find_survey_by_id(surveyid)
        if survey == None:
            return {'message': " Cannot generate summery. Surveyid '{}' does not exist".format(surveyid)}, 400 #bad request

        #second: generate a list of report objects to a specific survey id
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()

        #third: count histogram and determine counts
        evaluation = Auxiliary.counting_histogram_values(qid,reports)
        summed_answers = (evaluation['histogram'])
        count_answers = (evaluation['counts'])

        #fourth: determine other values for generating a summary:
        infos_from_reports = Auxiliary.extract_from_reports(qid,reports)
        report_name = infos_from_reports['name']
        report_options = infos_from_reports['options']

        infos_from_survey = Auxiliary.extract_from_surveys(qid,survey)
        survey_name = infos_from_survey['name']
        survey_type = infos_from_survey['type']
        survey_options = infos_from_survey['options']

        #fifth: if a prior summary already exists delete it, before writing the new one.
        old_smmry = SummaryModel.find_unique_summary(surveyid,qid)

        if old_smmry:
            old_smmry.delete_from_db()

        #6th: write the new summary:
        smmry = SummaryModel(qid,surveyid,report_name,survey_type,json.dumps(survey_options),json.dumps(summed_answers),count_answers)

        try:
            smmry.save_to_db()
        except:
            return {'message': "Error while saving summary."}, 500 #internal server error

        return smmry
