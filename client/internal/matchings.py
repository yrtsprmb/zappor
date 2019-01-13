#internal/matchings.py
import json

#############################################################
# operates on all answer and question inquiries
# takes whole dictionairies as input
# returns a list of matches from server and client questions
# in the following form:
# {'qid': 3, 'surveyid': 'digitalhelga', 'name': 'mtu'},
#############################################################


def find_matches(client,server):
    '''
    Find all matching inquiries and
    Takes all available inquiries from client and server and match them together.
    Stores the matches in a list which is returned.
    '''
    def compare_data(c, s, results):
        '''
        Compare client inquiries with server inquieres and returns matching qids.
        '''
        if (c.name == s.name and
            c.type == s.type and
            sorted(c.options) == sorted(s.options)):
            # data from client and server inquiries are gone be mixed here
            #results.append({'surveyid': s["surveyid"], 'qid': s["qid"], 'question': s["name"], 'options': c["randomanswer"], 'f': c["f"], 'p': c["p"], 'q': c["q"] })
            #results.append({'surveyid': s.surveyid, 'qid': s.qid, 'question': s.name, 'options': c.irr_answer, 'f': c.f, 'p': c.p, 'q': c.q })
            results.append({'surveyid': s.surveyid, 'qid': s.qid, 'question': s.name, 'options': json.loads(c.irr_answer), 'f': c.f, 'p': c.p, 'q': c.q })
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
