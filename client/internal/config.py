#internal/config.py

'''
Configuration settings
'''

secretkey_config = 'zappor'

#serviceprovider data
server = 'http://127.0.0.1'
port = '5000'
serviceprovider_reports = server + ':' + port + '/reports/'
serviceprovider_surveys = server + ':' + port + '/availablesurveys'


#timing of threads in seconds
repeat_request_surveys = 10
repeat_send_reports = 15

#global fpq settings are taken from the RAPPOR paper
global_f = 0.5 # delete in future
global_p = 0.75 # delete in future
global_q = 0.5 # delete in future


configfile_server = 'http://127.0.0.1'
configfile_port = '5000'

configfile_repeat_send_reports = 15
configfile_repeat_request_surveys = 10

configfile_f = 0.5
configfile_p = 0.75
configfile_q = 0.5

#global privacy settings
locked_config = True    #determines if incoming questions are locked by the client
quizmode_config = True  #if True incoming inquiries will be made to client inquiries

#gdpr/dsgvo
configfile_dsgvo = False

#print(serviceprovider_reports) #debug
#print(serviceprovider_surveys) #debug
