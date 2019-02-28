

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


## For first usage:
Please note that the sqllite tables will be created after startup with the first request which is made.
After first start, open always the homepage first and make a request to avoid sqllite errors.

Also consider, that you can't edit any client inquiries without consent to the data protection assignement. 
You can do this over the REST-endpoint for client-configuration or in the WEB GUI under settings tab.

Keep in mind that the client behaves differently in firefox and safari browsers. For more information on that, see the part 'Nuterstudie' in my thesis.


## Description
See section 'prototyp' in my thesis.