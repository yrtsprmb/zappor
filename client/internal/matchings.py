#internal/matchings.py
import json

def find_matches(client,server):
    '''
    Find all matching inquiries and
    Takes all available inquiries from client and server and match them together.
    Stores the matches in a list which is returned.
    '''
    def compare_data(c, s, results):
        '''
        Compares client inquiries with server inquieres.
        Returns the results after matching between the question.fdsa
        Because of One-Time RAPPOR, the PRR answer is chosen.
        '''
        if (c.name == s.name and
            c.type == s.type and
            sorted(c.options) == sorted(s.options)):
            # data from client and server inquiries are gone be mixed here
            #results.append({'surveyid': s["surveyid"], 'qid': s["qid"], 'question': s["name"], 'options': c["randomanswer"], 'f': c["f"], 'p': c["p"], 'q': c["q"] })
            #results.append({'surveyid': s.surveyid, 'qid': s.qid, 'question': s.name, 'options': c.irr_answer, 'f': c.f, 'p': c.p, 'q': c.q })
            results.append({'surveyid': s.surveyid, 'qid': s.qid, 'question': s.name, 'options': json.loads(c.prr_answer), 'f': c.f, 'p': c.p, 'q': c.q })
            return True
        else:
            return False

    results = []
    #for q in client['inquiries']:
    #    for p in server['inquiries']:
    for q in client:
        for p in server:
            r = compare_data(q, p, results)

    return results


def find_matching_surveys(items):
    '''
    Returs a list with with matching surveyids.
    '''
    results = []
    for item in items:
        if item['surveyid'] not in results:
            results.append(item['surveyid'])
    return(results)


def generate_answers_by_surveyid(surveyid,results):
    '''
    Returns answers in form of a list filled with dictionaries.
    '''
    answers = []
    for entry in results:
        answerentry = {}
        if surveyid == entry['surveyid']:

            answerentry['qid'] = entry['qid']
            answerentry['question'] = entry['question']
            answerentry['options'] = entry['options']
            answerentry['f'] = entry['f']
            answerentry['p'] = entry['p']
            answerentry['q'] = entry['q']
            answers.append(answerentry)
    return answers


# testing
# # #1) match client and server inquiries
# matches = find_matches(clienttest,servertest)
# print(matches)
# print("++++++++++++++++++++++++")
#
# # # 2) identify all surveyids which have an match
# surveys = allmatchingsurveys(matches)
# print("surveys with matches")
# print(surveys)
#
# # 3) generate answers by surveyid
# print("++++++++++++++++++++++++")
# ergebnis = generate_answers_by_surveyid('matchtest',matches)
# print(ergebnis)
