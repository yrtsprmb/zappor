import json
from flask_restful import Resource, reqparse

from models.client_inquiries import ClientInquiriesModel

#REST API to Access the client questions with their answers
class ClientInquiries(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=False,
        help="name error through parsing"
    )
    parser.add_argument('type',
        type=str,
        required=True,
        help="liste is missing"
    )
    parser.add_argument('options',
        type=str,
        action='append',
        required=True,
        help="options are missing"
    )
    parser.add_argument('answer',
        type=int,
        action='append',
        required=True,
        help="answer is missing"
    )
    parser.add_argument('randomanswer',
        type=int,
        action='append',
        required=True,
        help="randomanswer is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=True,
        help="locked option is missing"
    )
    parser.add_argument('f',
        type=float,
        required=True,
        help="f value is missing"
    )
    parser.add_argument('p',
        type=float,
        required=True,
        help="p value is missing"
    )
    parser.add_argument('q',
        type=float,
        required=True,
        help="q value is missing"
    )

    def get(self,name):
        answer = ClientInquiriesModel.find_by_name(name)
        if answer:
            return answer.tojson()
        return {'message': "Inquiry with name'{}' not found in client-db".format(name)}, 404 #not found

    def post(self,name):
        if ClientInquiriesModel.find_by_name(name):
            return {'message': "Inquiry with name '{}' already exist in client-db.".format(name)}, 400 #bad request
            #schreibe zeugs in db
        data = ClientInquiries.parser.parse_args()
        answer = ClientInquiriesModel(name,
                                data['type'],
                                json.dumps(data['options']),
                                json.dumps(data['answer']),
                                json.dumps(data['randomanswer']),
                                data['locked'],
                                data['f'],
                                data['p'],
                                data['q'])
        try:
            answer.save_to_db()
        except:
            return {'message': "error while inserting answer '{}'.".format(name)}, 500 #internal server error
        return answer.tojson(), 201 #created


    def put(self,name):
        data = ClientInquiries.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change - inquiry '{}' does not exist".format(name)}, 400 #bad request

        inquiry.type = data['type']
        inquiry.options = json.dumps(data['options'])
        inquiry.answer = json.dumps(data['answer'])
        inquiry.randomanswer = json.dumps(data['randomanswer'])
        inquiry.locked = data['locked']
        inquiry.f = data['f']
        inquiry.p = data['p']
        inquiry.q = data['q']

        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while editing inquiry with name: '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 202 # accepted
        #return {'message': "Sucessfully changend inquiry with name '{}'.".format(name)}, 400 #bad request


    def delete(self,name):
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry:
            inquiry.delete_from_db()
            return {'message': "client inquiry '{}' deleted".format(name)}, 202 #accepted
        return {'message': "client inquiry '{}' not found".format(name)}, 404 #not found

class ListClientInquiries(Resource):
    def get(self):
        return {'inquiries': [ x.tojson() for x in ClientInquiriesModel.query.all()]}


# allows to change the status of an inquiry through a GUI
# a user can change his answer, f,p and q values, as well if he wants to lock the question
class EditClientInquiries(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('answer',
    type=int,
    action='append',
    required=False,
    help="answer is missing"
    )
    parser.add_argument('locked',
        type=bool,
        required=False,
        help="status is missing or not correct"
    )
    parser.add_argument('f',
        type=float,
        required=False,
        help="status is missing or not correct"
    )
    parser.add_argument('p',
        type=float,
        required=False,
        help="status is missing or not correct"
    )
    parser.add_argument('q',
        type=float,
        required=False,
        help="status is missing or not correct"
    )
    def put(self,name):
        data = EditClientInquiries.parser.parse_args()
        inquiry = ClientInquiriesModel.find_by_name(name)
        if inquiry is None:
            return {'message': "Can not change status, inquiry '{}' does not exist".format(name)}, 400 #bad request

        inquiry.answer = json.dumps(data['answer'])
        inquiry.locked = data['locked']
        inquiry.f = data['f']
        inquiry.p = data['p']
        inquiry.q = data['q']
        try:
            inquiry.save_to_db()
        except:
            return {'message': "error while saving inquiry with name: '{}'.".format(name)}, 500 #internal server error
        return inquiry.tojson(), 200 #ok
        #return {'message': " inquiry '{}' changed.".format(name)}, 200 #ok
