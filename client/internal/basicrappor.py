import random


f = 0.5
p = 0.75
q = 0.5

test = [0,1,0,1,0]



#############################################################
# takes the f value and an ordinal list of 0 and 1 digits,
# returns the PRR of that list.
#############################################################

def permanent_RandomizedResponse(f,original_list):

    a = 0.5 * f # probability of appending a 1
    b = 0.5 * f # propability of appending a 0
    c = 1-f     # probability that the bit will not changed (true answer)
    prr = []
    for i in original_list:
        i = random.choices([0, 1, i], [a, b, c])
        prr.append(i[0])
    return prr


#############################################################
# # Compute Instantaneous Randomized Response (IRR).
# # If PRR bit is 0, IRR bit is 1 with probability p.
# # If PRR bit is 1, IRR bit is 1 with probability q.
#############################################################

def instantaneous_RandomizedResponse(p,q,prr_list):

    irr = []
    for i in prr_list:
        if i == 1:
            i = random.choices([0, 1], [1-q,q])

        else:
            i = random.choices([0, 1], [p,1-p])

        irr.append(i[0])
    return irr


horst = permanent_RandomizedResponse(0.3,[0,1])

#tests
#horst = instantaneous_RandomizedResponse(0.5,0,[0,0,0,0])
print(horst)
