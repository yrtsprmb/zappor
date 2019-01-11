#internal/matchings.py
import json

#############################################################
# operates on all answer and question inquiries
# takes whole dictionairies as input
# returns a list of matches from server and client questions
# in the following form:
# {'qid': 3, 'surveyid': 'digitalhelga', 'name': 'mtu'},
#############################################################


# def check_correctness(client,server):
#     # should check if the values are correct
#     pass


def find_matches(client,server):
    '''
    TODO: should return an evaluation of allreports belonging to a surveyidself.
    '''
    # compare client inquiries with server inquieres and returns matching qids
    def compare_data(c, s, results):
        #c['name'] == s['name'] and
        #c['type'] == s['type'] and
        #sorted(c['options']) == sorted(s['options'])
        # print("test")
        # print(c.options)
        # print(type(c.options))
        # print(s.options)
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

#############################################################
# returs a list with surveyids which have matches
#############################################################
def find_matching_surveys(items):
    results = []
    for item in items:
        if item['surveyid'] not in results:
            results.append(item['surveyid'])
    return(results)


#############################################################
# returns answers in form of list filled with dictionaries
#############################################################
def generate_answers_by_surveyid(surveyid,results):
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


###########################################################

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
