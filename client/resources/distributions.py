#resources/simulate
import json
from flask_restful import Resource
from flask import request
from models.client_inquiries import ClientInquiriesModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
import math
from random import randint


class Distribution(Resource):
    '''
    Simualates a distribution
    '''
    def get(self):
        a = []
        b = []

        for i in range(8):
            a.append(randint(100, 500))
            b.append(randint(100, 500))



        return {'data1': a, 'data2': b}, 200, {'Access-Control-Allow-Origin': '*'}


class DistributionAll(Resource):
    '''
    Simualates a distribution for all inquiries
    '''
    def get(self,inq):
        # find inquiry
        if not ClientInquiriesModel.find_by_name(inq):
            return {'message': "no inquiry with that name"}, 200 #ok

        inquiry = ClientInquiriesModel.find_by_name(inq)

        # values from the object
        buckets = len(json.loads(inquiry.answer))
        answer = json.loads(inquiry.answer)
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
        'epsilon': epsilon_prr
        }, 200, {'Access-Control-Allow-Origin': '*'}





class Simulate(Resource):
    '''
    Simualates a distribution
    '''
    def get(self,inq):
        '''
        test
        '''
        # find inquiry
        if not ClientInquiriesModel.find_by_name(inq):
            return {'message': "no inquiry with that name"}, 200 #ok

        inquiry = ClientInquiriesModel.find_by_name(inq)

        users = 500
        buckets = 6
        own_option = [0,0,1,0,0,1]

        f = 0.001

        world_one_container_without = []

        #create world one without user as array (n-1 users) and fill it with random values
        for x in range(users):
            histogram = [0]* (buckets-1)
            index = randint(0,buckets-1)
            histogram.insert(index,1)
            print('histogram')
            print(histogram)
            world_one_container_without.append(histogram)

        #create world one within
        world_one_container_within = world_one_container_without.copy()
        world_one_container_within.append(own_option)

        members_without = len(world_one_container_without)
        members_within = len(world_one_container_within)

        # print("container world one without")
        # print(world_one_container_without)
        # print(len(world_one_container_without))
        # print("container world one within")
        # print(world_one_container_within)
        # print(len(world_one_container_within))


        #sum up world one without
        world_one_without = [0]* buckets
        for elem in world_one_container_without:
            print("step1")
            print(world_one_without)
            print("step1 add")
            print(elem)
            world_one_without = [x + y for x,y in zip(world_one_without,elem)]
            print("step2")
            print(world_one_without)

        world_one_within = [0]* buckets
        for elem in world_one_container_within:
            world_one_within = [x + y for x,y in zip(world_one_within,elem)]


        # create world 2 container without user
        world_two_container_without = []
        for elem in world_one_container_without:
            new = permanent_RandomizedResponse(f,elem)
            world_two_container_without.insert(-1,new)

        # create world 2 container within user
        world_two_container_within = world_two_container_without.copy()
        world_two_container_within.insert(-1,permanent_RandomizedResponse(f,own_option))

        # # create world 2 container within user (total new)
        # world_two_container_within = []
        # for elem in world_one_container_without:
        #     new = permanent_RandomizedResponse(f,elem)
        #     world_two_container_without.insert(-1,new)



        print("container world two without")
        print(world_two_container_without)
        print("container world two within")
        print(world_two_container_within)

        #sum up world two without
        world_two_without = [0]* buckets
        for elem in world_two_container_without:
            world_two_without = [x + y for x,y in zip(world_two_without,elem)]

        #sum up world two within
        world_two_within = [0]* buckets
        for elem in world_two_container_within:
            world_two_within = [x + y for x,y in zip(world_two_within,elem)]

        epsilon_prr = 2 * (math.log((1 - (0.5 * f)) / (0.5 * f)))


        return {'privacy demo': "zepp privacy",
            'buckets': buckets,
            'own option': own_option,
            'members within': members_within,
            'members without': members_without,
            'scenario1 with user': world_one_within, #original_opt_in,
            'scenario1 without user': world_one_without, #original_opt_out,
            'scenario2 within user': world_two_within, #original_opt_out,
            'scenario2 without user': world_two_without, #original_opt_out,
            'f': f,
            'epsilon': epsilon_prr
        }
