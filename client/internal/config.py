#internal/config.py

'''
Configuration settings
'''

secretkey_config = 'zappor'

'''
Configuration data for the connection to the server.
'''
configfile_server = 'http://127.0.0.1'
configfile_port = '5000'
#server = 'http://127.0.0.1'
#port = '5000'
serviceprovider_reports = configfile_server + ':' + configfile_port + '/reports/'
serviceprovider_surveys = configfile_server + ':' + configfile_port + '/availablesurveys'


'''
Timing of threads in seconds.
'''
# determines how often surveys are requested in seconds.
repeat_request_surveys = 100
# determines how often reports are sent in seconds.
repeat_send_reports = 150


configfile_repeat_send_reports = 15
configfile_repeat_request_surveys = 10

# global fpq settings are taken from the RAPPOR paper.
# https://doi.org/10.1145/2660267.2660348
configfile_f = 0.5
configfile_p = 0.75
configfile_q = 0.5

# global privacy settings
locked_config = True    #determines if incoming questions are locked by the client

# if quizmode_config is set to 'True', incoming survey questions will also stored in client inquiries.
quizmode_config = True

# gdpr/dsgvo
configfile_dsgvo = False
