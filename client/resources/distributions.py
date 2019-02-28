#resources/simulate
import json
from flask_restful import Resource
from flask import request
from models.client_inquiries import ClientInquiriesModel
from models.simulations import SimulationModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
import math
from random import randint


class DistributionAll(Resource):
    '''
    Simualates a PRR distribution for a specific client inquiry for the GUI.
    '''
    def get(self,inq):
        '''
        Takes the name of on inquiry and returns the distribution in JSON format.
        '''
        # find inquiry
        if not ClientInquiriesModel.find_by_name(inq):
            return {'message': "no inquiry with that name"}, 400 #bad request


        inquiry = ClientInquiriesModel.find_by_name(inq)

        # values from the object
        buckets = len(json.loads(inquiry.answer))
        answer = json.loads(inquiry.answer)
        answer_buckets = [i for i, x in enumerate(answer) if x == 1]

        #f = inquiry.f
        f = float(request.args.get('f'))
        users = 100

        #create original world one without user as array (n-1 users) and fill it with random values
        original_opt_out = []
        for x in range(users):
            histogram = [0]* (buckets-1)
            index = randint(0,buckets-1)
            histogram.insert(index,1)
            #print('histogram')
            #print(histogram)
            original_opt_out.append(histogram)

        #create original world with own answer
        original_opt_in = original_opt_out.copy()
        original_opt_in.append(answer)


        random_opt_out = []
        ###random without
        for element in original_opt_out:
            new = permanent_RandomizedResponse(f,element)
            random_opt_out.insert(-1,new)




        # sum up original world without
        original_without = [0]* buckets
        for elem in original_opt_out:
            #print("step1")
            #print(original_without)
            #print("step1 add")
            #print(elem)
            original_without = [x + y for x,y in zip(original_without,elem)]
            #print("step2")
            #print(original_without)

        # for k, v in enumerate(original_without):
        #     original_without[k] = v/users

        # sum up original world within
        original_within = [0]* buckets
        for elem in original_opt_in:
            original_within = [x + y for x,y in zip(original_within,elem)]

        # for k, v in enumerate(original_within):
        #     original_within[k] = v/(users+1)

        #create random world without user as array (n-1 users) and fill it with random values
        # random_opt_out = []
        # for x in range(users):
        #     histogram = [0]* (buckets-1)
        #     index = randint(0,buckets-1)
        #     histogram.insert(index,1)
        #     #print("zepp")
        #     #print(histogram)
        #     random_histogram = permanent_RandomizedResponse(f,histogram)
        #     #print(random_histogram)
        #     random_opt_out.append(random_histogram)

        # sum up random world without
        random_without = [0]* buckets
        for elem in random_opt_out:
            random_without = [(x + y) for x,y in zip(random_without,elem)]

        # for k, v in enumerate(random_without):
        #     random_without[k] = v/users
        #print(random_without)



        #create random world within user as array (n-1 users) and fill it with random values
        # random_opt_in = []
        # for x in range(users):
        #     histogram = [0]* (buckets-1)
        #     index = randint(0,buckets-1)
        #     histogram.insert(index,1)
        #     #print("zepp")
        #     #print(histogram)
        #     random_histogram = permanent_RandomizedResponse(f,histogram)
        #     #print(random_histogram)
        #     random_opt_in.append(random_histogram)
                # randomanswer = permanent_RandomizedResponse(f,answer)
                # random_opt_in.append(randomanswer)

        random_opt_in = random_opt_out.copy()
        random_histogram = permanent_RandomizedResponse(f,answer)
        random_opt_in.append(random_histogram)
        print("horst")
        print(len(random_opt_in))



        # sum up random world within
        random_within = [0]* buckets
        for elem in random_opt_in:
            random_within = [(x + y) for x,y in zip(random_within,elem)]

        # for k, v in enumerate(random_within):
        #     random_within[k] = v/(users+1)

        #print(random_within)

        users_opt_in = len(original_opt_in)
        users_opt_out = len(original_opt_out)


        print("original_without")
        print(original_without)
        print("original_within")
        print(original_within)

        print("users_opt_in")
        print(users_opt_in)
        print("users_opt_out")
        print(users_opt_out)
        print("privacy value f")
        print(f)
        print("random_without")
        print(random_without)
        print("random_within")
        print(random_within)

        epsilon_prr = 2 * (math.log((1 - (0.5 * f)) / (0.5 * f)))
        print("epsilon")
        print(epsilon_prr)

        return {
        'original_without': original_without,
        'original_within': original_within,
        'random_without': random_without,
        'random_within': random_within,
        'epsilon': epsilon_prr,
        'answer_buckets': answer_buckets
        }, 200, {'Access-Control-Allow-Origin': '*'}


class DistributionRest(Resource):
    '''
    Simualates a PRR distribution for a specific client inquiry for the REST Api.
    '''
    def get(self,name):
        '''
        Takes the name of on inquiry and returns the distribution in JSON format.
        '''
        # find inquiry
        if not ClientInquiriesModel.find_by_name(name):
            return {'message': "no inquiry with that name"}, 400 #bad request

        inquiry = ClientInquiriesModel.find_by_name(name)

        # values from the object
        buckets = len(json.loads(inquiry.answer))
        answer = json.loads(inquiry.answer)
        f = inquiry.f
        users = 100

        #create original world one without user as array (n-1 users) and fill it with random values
        original_opt_out = []
        for x in range(users):
            histogram = [0]* (buckets-1)
            index = randint(0,buckets-1)
            histogram.insert(index,1)
            #print('histogram')
            #print(histogram)
            original_opt_out.append(histogram)

        #create original world with own answer
        original_opt_in = original_opt_out.copy()
        original_opt_in.append(answer)


        random_opt_out = []
        ###random without
        for element in original_opt_out:
            new = permanent_RandomizedResponse(f,element)
            random_opt_out.insert(-1,new)


        # sum up original world without
        original_without = [0]* buckets
        for elem in original_opt_out:
            #print("step1")
            #print(original_without)
            #print("step1 add")
            #print(elem)
            original_without = [x + y for x,y in zip(original_without,elem)]
            #print("step2")
            #print(original_without)

        # for k, v in enumerate(original_without):
        #     original_without[k] = v/users

        # sum up original world within
        original_within = [0]* buckets
        for elem in original_opt_in:
            original_within = [x + y for x,y in zip(original_within,elem)]


        # sum up random world without
        random_without = [0]* buckets
        for elem in random_opt_out:
            random_without = [(x + y) for x,y in zip(random_without,elem)]


        random_opt_in = random_opt_out.copy()
        random_histogram = permanent_RandomizedResponse(f,answer)
        random_opt_in.append(random_histogram)

        print(len(random_opt_in))

        # sum up random world within
        random_within = [0]* buckets
        for elem in random_opt_in:
            random_within = [(x + y) for x,y in zip(random_within,elem)]


        epsilon_prr = 2 * (math.log((1 - (0.5 * f)) / (0.5 * f)))

        return {
        'name': inquiry.name,
        'answer': inquiry.answer,
        'users without': users,
        'users withint': users + 1,
        'answer': inquiry.answer,
        'original_without': original_without,
        'original_within': original_within,
        'random_without': random_without,
        'random_within': random_within,
        'f': f,
        'epsilon': epsilon_prr
        }, 200 # status ok

class DistributionIRR(Resource):
    '''
    Simualates an IRR distribution for a specific client inquiry for the GUI.
    '''
    def get(self,name):
        '''
        Takes the name of on inquiry and returns with every refresh a new IRR of the data.
        '''
        # find inquiry
        if not ClientInquiriesModel.find_by_name(name):
            return {'message': "no inquiry with that name"}, 400 #bad request


        inquiry = ClientInquiriesModel.find_by_name(name)
        p = inquiry.p
        q = inquiry.q
        answer_prr = json.loads(inquiry.answer)
        #answer_prr = json.loads(inquiry.prr_answer)
        answer_irr = instantaneous_RandomizedResponse(p,q,answer_prr)
        #epsilon_prr = 2 * (math.log((1 - (0.5 * f)) / (0.5 * f)))
        empty = 0

        simulation = SimulationModel.find_by_name(name)
        if simulation is None:
            s = SimulationModel(name)
            s.added_irr = json.dumps([0.0]* len(answer_irr))
            s.average_irr = json.dumps([0.0]* len(answer_irr))
            s.save_to_db()
            return {
            'name': inquiry.name
            }, 200 # status ok

        simulation.count = simulation.count + 1

        irr_sum = [x + y for x,y in zip(answer_irr,json.loads(simulation.added_irr))]
        simulation.added_irr = json.dumps(irr_sum)
        simulation.save_to_db()

        new_average = [0]* len(answer_irr)
        #for x in new_average:

        #test = map(/simulation.count,irr_sum)
        test = list(map(lambda x: x/simulation.count,irr_sum))

        print("test")
        print(test)


        print("simulation")
        print(simulation)


        return {
        'name': inquiry.name,
        'number of reports': simulation.count,
        'irr_added': simulation.added_irr,
        'irr_average': simulation.average_irr,
        'answer_prr': answer_prr,
        'answer_irr': answer_irr,
        'rolling_irr' : test
        }, 200 # status ok

        # return {
        # 'name': inquiry.name,
        # 'number of reports': simulation.count,
        # 'irr_added': simulation.added_irr,
        # 'irr_average': simulation.average_irr,
        # 'answer': answer,
        # 'answer_prr': answer_prr,
        # 'answer_irr': answer_irr,
        # 'f': inquiry.f,
        # 'p': inquiry.p,
        # 'q': inquiry.q,
        # 'epsilon': epsilon_prr,
        # 'test': empty
        # }, 200 # status ok


    def delete(self, name):
        if not SimulationModel.find_by_name(name):
            return {'message': "no simulation with that name"}, 400 #bad request

        SimulationModel.find_by_name(name).delete_from_db()

        return {
            'deleted': name
        }, 200
