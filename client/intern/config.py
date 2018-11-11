#intern/config.py

## configurations ##


#serviceprovider data
server = 'http://127.0.0.1'
port = '5000'
serviceprovider_reports = server + ':' + port + '/reports/'
serviceprovider_surveys = server + ':' + port + '/availablesurveys'


#timing of threads in seconds
repeat_request_surveys = 10
repeat_send_reports = 15



#global RAPPOR client settings
global_prr = 1
global_irr = 1

global_f = 0.75
global_p = 0.5
global_q = 0.5





#print(serviceprovider_reports) #debug
#print(serviceprovider_surveys) #debug
