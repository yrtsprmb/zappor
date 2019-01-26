

## Installation & Startup

First create a new python environment.
Go to the folder where you want to use the application and type the following command to create a virtual environment for python 3:
'virtualenv venv --python=python3'

Then you are able to start you virtual environment with the following command:
'source venv/bin/activate'

When your environment is active use the 'requirements.txt' file for installing the required python packages:
'pip install -r requirements.txt'

To deactivate the virtual environment type:
'deactivate'

After the environment is set up and the requirements are installed you can start client & server in their responding folder with:
'python app.py'

After starting, you can reach the WEB GUI in the browser under the following URL:

Client: http://localhost:5001
Server: http://localhost:5001


For first usage:
Please note that the sqllite tables will be created after startup with the first request which is made.
Also consider, that you can't edit client inquiries without consent to the GDPR assignement. 
You can do this over the requests for the configuration or in the WEB GUI under settings.

## Description


Ports can be changed in the responsible internal/config.py file.

## Implementation
Thanks to...  for....