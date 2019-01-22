#internal/config.py
'''
Configuration settings
'''

secretkey_config = 'zappor'

'''
Configuration for the server connection.
'''
serveraddress_config = 'http://127.0.0.1'
serverport_config = '5000'
config_server = serveraddress_config + ':' + serverport_config

serviceprovider_reports = config_server + '/reports/'
serviceprovider_surveys = config_server + '/availablesurveys'


'''
Configuration for local client.
'''
clientaddress_config = 'http://127.0.0.1'
clientport_config = '5001'
config_client = clientaddress_config + ':' + clientport_config


'''
Timing of threads in seconds.
'''
# determines how often surveys are requested in seconds.
repeat_request_surveys = 100
# determines how often reports are sent in seconds.
repeat_send_reports = 150


config_repeat_send_reports = 15
config_repeat_request_surveys = 10



'''
Global privacy settings.
'''
# global fpq settings are taken from the RAPPOR paper.
# https://doi.org/10.1145/2660267.2660348
config_f = 0.5
config_p = 0.75
config_q = 0.5

# g
config_locked = True    #determines if incoming questions are locked by the client

# if quizmode_config is set to 'True', incoming survey questions will also stored in client inquiries.
config_quizmode = True

# gdpr/dsgvo
config_dsgvo = False
