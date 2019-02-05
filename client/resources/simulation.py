#resources/simulate
import json
from flask_restful import Resource
from models.server_inquiries import ServerInquiriesModel
from models.client_inquiries import ClientInquiriesModel
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
import math
from random import randint


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

        users = 10
        buckets = 5
        own_option = [0,0,1,0,0]

        f = 0.5
        p = 0.75
        q = 0.5

        world_one_container_without = []
        world_two = []

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
            'world1 with user': world_one_within, #original_opt_in,
            'world1 without user': world_one_without, #original_opt_out,
            'world2 within user': world_two_within, #original_opt_out,
            'world2 without user': world_two_without, #original_opt_out,
            'f': f,
            'epsilon': epsilon_prr
        }

# #gib an wie viele optionen (breite des arrays)
# #gib an wieviele teilnehmer
#
# erstelle eine liste mit listen.
#
#
#
#
#     #create 5000 of them
#         print(inquiry)
#         #print(inquiry.answer)
#         print(type(inquiry))
#
#         print(inquiry.answer)
#         #print(inquiry.answer)
#         print(type(json.loads(inquiry.answer)))
#
#         answer = json.loads(inquiry.answer)
#         prr = json.loads(inquiry.prr_answer)
#         irr = json.loads(inquiry.irr_answer)
#         f = inquiry.f
#         p = inquiry.p
#         q = inquiry.q
#         buckets = len(json.loads(inquiry.answer))
#         # print(g)
#         # print(type(g))
#
#         histogram_prr = [0]* buckets
#         histogram_irr = [0]* buckets
#
#         counts = 200
#         first_prr = permanent_RandomizedResponse(f,answer)
#
#         #prr berechnen
#         for x in range (0,counts):
#             new = permanent_RandomizedResponse(f,answer)
#             #print(new)
#             histogram_prr = [x + y for x,y in zip(histogram_prr,new)]
#
#         print("-------------------------------------")
#         print(histogram_prr)
#
#         #irr berechnen
#         for x in range (0,counts):
#              new_irr = instantaneous_RandomizedResponse(p,q,first_prr)
#              #new_irr = instantaneous_RandomizedResponse(p,q,answer)
#              #print(new)
#              histogram_irr = [x + y for x,y in zip(histogram_irr,new_irr)]
#              #print(histogram)
#              #print("-------------------------------------")
#         print("-------------------------------------")
#         print(histogram_irr)

        #
        # z = 0.99
        # prrepsilon = 2 * math.log((1 - (0.5 * z)) / (0.5 * z))
        # print("epsilon prr for f " + str(z))
        # print(prrepsilon)
        #
        # epsilon_prr = 2 *  (math.log((1 - (0.5 * f)) / (0.5 * f)))
        # epsilon_irr = prrepsilon

        #zepp = 2* math.ln( 1 - 0.5 * f / 0.5 * f)
        # users = 100
        # original_opt_in [25,25,40,10]
        # original_opt_out [25,25,39,10]
        #
        # random_opt_in [25,25,40,10]
        # random_opt_out [25,25,39,10]
        #
        # f = 0.5
        # p = 0.75
        # q = 0.5
        #
        #
        # return {'privacy demo': "zepp privacy",
        #     'users': users,
        #     'with user': original_opt_in,
        #     'without user': original_opt_out,
        #     'rappor with user': random_opt_in,
        #     'rappor without user': random_opt_out,
        #     'value p': f,
        #     'value p': p,
        #     'value q': q,
        # }

        #return {'message': "histogram after {} counts with value f {} : {}.".format(counts,f,histogram)},200 #ok
