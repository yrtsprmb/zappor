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
        # print(answer)
        print(buckets)
        counts = 100000
        f = 0.1
        histogram = [0,0,0,0,0,0,0]
        for x in range (0,counts):
            new = permanent_RandomizedResponse(f,answer)
            #print(new)
            histogram = [x + y for x,y in zip(histogram,new)]
            #print(histogram)
            #print("-------------------------------------")

        print(histogram)
        # first = [0,0,0,0,0,8,0]
        # second = [0,0,0,0,0,8,0]
        # print([x + y for x,y in zip(first,second) ])
        return {'message': "histogram after {} counts with value f {} : {}.".format(counts,f,histogram)},200 #ok
