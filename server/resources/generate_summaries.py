#resources/generate_summaries.py

import json
from flask_restful import Resource
from models.report import ReportModel
from models.summaries import SummaryModel
from internal.evaluation import list_answers, extract_qids, extract_qid_info, extract_qid_info2

from internal.evaluation import counting_histogram_values_new

class GenerateSummaries(Resource):
    '''
    TODO: Should return an evaluation of a qid belonging to a specific survey.
    Tooks all reports belonging to a surveyid / qid combination and generates a new summary.
    If there exists already a summary, the old one will be overwritten.
    '''

    def get(self,surveyid):
        '''
        TODO: should return an evaluation of allreports belonging to a surveyidself.
        This
        '''


        #2er Schritt: Hole alle reports zu einer surveyid

        #generates a list of report objects to a specific survey id
        reports = ReportModel.query.filter_by(surveyid=surveyid).all()
        print("Report Models")
        print(reports) #debug
        print("------------------------------------------")

        #generate a list of list answers, which contains dictionaries
        listofanswers = list_answers(reports) #works

        #answerlist = (json.loads(report.answers))

        qid = 34

        summed_answer = counting_histogram_values_new(qid,reports)
        print(summed_answer)
        print(type(summed_answer))

        # Vorletzer Schritt:
        # Liegt einee summary zu einer surveyid qid Kombination bereits vor, lösche diese.





        # Letzter Schritt: schreibe eine summary zu einer qid in die datenbank in die datenbank:
        # funktioniert so wie hier beschrieben

        #qid: wird uebergeben
        #surveyid: wird uebergeben
        #name -> muss extrahiert werden
        #typ -> brauche ich den?
        #options -> muss extrahiert werden
        #answers -> nehme ich aus summed_answer

        print(surveyid)

        #smmry = SummaryModel(qid,surveyid,name,type,json.dumps(options),json.dumps(summed_answers))




        qid = 88
        surveyid = "surveyid"
        name = "horsthorst"
        typ = "ordinal"
        options = ["malte","kelly"]
        answers = [0,1]
        counter = 125

        smmry = SummaryModel(qid,surveyid,name,typ,json.dumps(options),json.dumps(answers))

        #try:
        smmry.save_to_db()
        #except:
        #    return {'message': "Error while saving summary."}, 500 #internal server error


        return {'message': " '{}' ".format(surveyid)}, 200 #ok
        #return {'message': " evaluation done."}, 200 #ok
