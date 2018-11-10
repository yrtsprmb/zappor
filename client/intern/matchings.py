import json

client = {
    "inquiries": [
        {
            "name": "lrz",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c",
                "d"
            ],
            "answer": [
                0,
                1,
                0,
                1
            ],
            "randomanswer": [
                0,
                1,
                0,
                1
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        },
        {
            "name": "bmw",
            "type": "ordinal",
            "options": [
                "d",
                "e",
                "f"
            ],
            "answer": [
                "0",
                "1",
                "0"
            ],
            "randomanswer": [
                0,
                1,
                1
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        },
        {
            "name": "mtu",
            "type": "numeric",
            "options": [
                "a",
                "b"
            ],
            "answer": [
                [23455.5]
            ],
            "randomanswer": [
                0,
                1,
                1
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        },
        {
            "name": "lmu",
            "type": "ordinal",
            "options": [
                "v",
                "w",
                "x",
                "y",
                "z"
            ],
            "answer": [
                1,
                0,
                0,
                0,
                0
            ],
            "randomanswer": [
                0,
                1,
                1,
                1,
                0
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        },
        {
            "name": "nintendo",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c"
            ],
            "answer": [
                1,
                0,
                1

            ],
            "randomanswer": [
                0,
                1,
                0
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        },
        {
            "name": "sega",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c"
            ],
            "answer": [
                1,
                0,
                1

            ],
            "randomanswer": [
                0,
                1,
                0
            ],
            "locked": 1,
            "f": 0.5,
            "p": 0.5,
            "q": 0.5
        }
    ]
}
###################################################

server = {
    "inquiries": [
        {
            "qid": 66,
            "surveyid": "analoghorsta",
            "serviceprovider": "radiohorsta",
            "name": "sega",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c"
            ]
        },
        {
            "qid": 88,
            "surveyid": "digitalhelga",
            "serviceprovider": "radiohorsta",
            "name": "sega",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c"
            ]
        },
        {
            "qid": 1,
            "surveyid": "digitalhelga",
            "serviceprovider": "radiohorsta",
            "name": "lrz",
            "type": "ordinal",
            "options": [
                "a",
                "b",
                "c"
            ]
        },
        {
            "qid": 2,
            "surveyid": "digitalhelga",
            "serviceprovider": "radiohorsta",
            "name": "bmw",
            "type": "ordinal",
            "options": [
                "d",
                "x",
                "f",
                "g"
            ]
        },
        {
            "qid": 3,
            "surveyid": "digitalhelga",
            "serviceprovider": "radiohorsta",
            "name": "mtu",
            "type": "ordinal",
            "options": [
                "a",
                "b"
            ]
        },
        {
            "qid": 4,
            "surveyid": "digitalhelga",
            "serviceprovider": "radiohorsta",
            "name": "lmu",
            "type": "ordinal",
            "options": [
                "v",
                "w",
                "x",
                "y",
                "z"
            ]
        }
    ]
}


#############################################################
# operates on all answer and question inquiries
# takes whole dictionairies as input
# returns a list of matches from server and client questions
# in the following form:
# {'qid': 3, 'surveyid': 'digitalhelga', 'name': 'mtu'},
#############################################################
def find_matches(client,server):
    # compare client inquiries with server inquieres and returns matching qids
    def compare_data(c, s, results):
        if (
                c['name'] == s['name'] and
                c['type'] == s['type'] and
                sorted(c['options']) == sorted(s['options'])):

            results.append({'surveyid': s["surveyid"], 'qid': s["qid"], 'question': s["name"], 'options': c["randomanswer"], 'f': c["f"], 'p': c["p"], 'q': c["q"] })
            return True
        else:
            return False

    results = []
    for q in client['inquiries']:
        for p in server['inquiries']:
            r = compare_data(q, p, results)

    return results

#############################################################
# returs a list with surveyids which have matches
#############################################################
def allmatchingsurveys(items):
    results = []
    for item in items:
        if item['surveyid'] not in results:
            results.append(item['surveyid'])
    return(results)



#############################################################
# returns answers in form of list filled with dictionairis
#############################################################
def generate_answers_by_surveyid(surveyid,results):
    answers = []
    for entry in results:  #geht auch mit ergebnis
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

#
# #1) match client and server inquiries
# matches = find_matches(client,server)
# print(matches)
# print("++++++++++++++++++++++++")
#
# # 2) identify all surveyids which have an match
# surveys = allmatchingsurveys(matches)
# print("surveys with matches")
# print(surveys)
#
# # 3) generate answers by surveyid
# print("++++++++++++++++++++++++")
# ergebnis = generate_answers_by_surveyid('analoghorsta',matches)
# print(ergebnis)
