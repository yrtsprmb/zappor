#resources/simulate
import json
from flask_restful import Resource
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from internal.basicrappor import permanent_RandomizedResponse


class Simulate(Resource):
    '''
    Simualates
    '''
    def get(self,inq):
        '''
        test
        '''
        # find inquiry
        if not ClientInquiriesModel.find_by_name(inq):
            return {'message': "no inquiry with that name"}, 200 #ok

        inquiry = ClientInquiriesModel.find_by_name(inq)
    #create 5000 of them
        print(inquiry)
        #print(inquiry.answer)
        print(type(inquiry))

        print(inquiry.answer)
        #print(inquiry.answer)
        print(type(json.loads(inquiry.answer)))

        answer = json.loads(inquiry.answer)
        prr = json.loads(inquiry.prr_answer)
        irr = json.loads(inquiry.irr_answer)
        buckets = len(json.loads(inquiry.answer))

        histogram = [0]* buckets
        print(histogram)
        print(buckets)
        counts = 10000
        f = 0.1

        for x in range (0,counts):
            new = permanent_RandomizedResponse(f,answer)
            #print(new)
            histogram = [x + y for x,y in zip(histogram,new)]
            #print(histogram)
            #print("-------------------------------------")

        # angenommen ich habe hier unten 2 bis 3 listen beliebiger länge (aber alle 3 sind gleich lang)
        # die möchte ich als histogramme darstellen, wobei ein listenelemet ein bucket darstellen.
        # so das ich sie neben oder vielleicht übeinander legen kann.
        # beispiel:
        #[503, 483, 534, 528, 481, 9459, 510]
        #[537, 531, 509, 504, 484, 9516, 546]
        #[514, 471, 527, 524, 470, 9530, 522]
        # die neben, bzw. hintereinaderlegen.

        return {'message': "histogram after {} counts with value f {} : {}.".format(counts,f,histogram)},200 #ok
