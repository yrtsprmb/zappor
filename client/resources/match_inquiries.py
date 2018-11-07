import json
from flask_restful import Resource, reqparse
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from models.reports import ReportModel

class MatchInquiries(Resource):
    def get(self):
        # nehme eine question aus der question.db und vergleiche die mit allen
        # in der answer.db vorliegenden fragen.
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
                        "0",
                        "1",
                        "0",
                        "1"
                    ],
                    "randomanswer": [
                        "0",
                        "1",
                        "0",
                        "1"
                    ],
                    "locked": 0,
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
                        "0",
                        "1",
                        "1"
                    ],
                    "locked": 0,
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
                        "23455.5"
                    ],
                    "randomanswer": [
                        "0",
                        "1",
                        "1"
                    ],
                    "locked": 0,
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
                        "1",
                        "0",
                        "0",
                        "0",
                        "0"
                    ],
                    "randomanswer": [
                        "0",
                        "1",
                        "1",
                        "1",
                        "0"
                    ],
                    "locked": 0,
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

        results = []
        # compare client inquiries with server inquieres and returns matching qids
        def compare_data(c, s, results):
            if (
                    c['name'] == s['name'] and
                    #c['type'] == s['type'] and
                    sorted(c['options']) == sorted(s['options'])):

                #results.append(s["qid"])
                #results.append(s["name"])
                results.append({'qid': s["qid"], 'surveyid': s["surveyid"], 'name': s["name"] })
                return True
            else:
                return False



        for q in client["inquiries"]:
            for p in server["inquiries"]:
                r = compare_data(q, p, results)

        print(results)


        ##############################################################
        # nimm resultierende qids

        ergebnis = [{'qid': 3, 'name': 'mtu'}, {'qid': 4, 'name': 'lmu'}]
        print(ergebnis)

        #baue einen report auf:
        #
        #
        #
        # baue einen teilreport zu frangen, wenn locked = false bei eigentlicher frage
        #
        #  if locked == False
        #qid aus antwortliste   ->    "qid": 1,
        #name aus antwortliste" -> question": "gender",
        #von client randomanswer: -> "options": [1,0,0],
        #von client f:	   "f":  0.5,
        #von client p:	   "p":  0.75,
        #von client q:	   "q":  0.5

        print('--------------------------------')

        for entry in results:  #geht auch mit ergebnis
            qid = entry['qid']
            name = entry['name']
            #answers =

            print(str(qid))
            print(name)

            for entry in (client['inquiries']):
                if name == entry['name']:
                    answers = entry['randomanswer']
                    f = entry['f']
                    p = entry['p']
                    q = entry['q']
                    print(answers)
                    print(str(f))
                    print(str(p))
                    print(str(q))
