from flask_restful import Resource, reqparse
from pymongo import *

client = MongoClient('mongodb+srv://PythonApp:4X0LUM8zjS7Q@researchcluster.usrji.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.research
collection = db.answers

var1 = 'gender'
var2 = 'age'
all_variables = [var1, var2]


class Answers(Resource):

    def get(self):
        all_documents = collection.find()
        list_document = list(all_documents)
        # change each element's _id type from 'bson.objectid.ObjectId' to 'str' to be returned to the final json view
        data = []
        for document in list_document:
            document['_id'] = str(document['_id'])
            data.append(document)
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', required=False)
        for var in all_variables:
            parser.add_argument(var, required=False)
        args = parser.parse_args()

        # creating new document
        new_data = {
            '_id': args['_id']
        }
        for var in all_variables:
            new_data[var] = args[var]

        # adding new document
        if len(args['_id']) == 24:
            if self.check_user_input(args[var2], var2) == 'number':
                if self.check_user_input(args[var1], var1) == 'string':
                    collection.update_one(new_data, {'$set': new_data}, upsert=True)
                    return self.get(), 200
                else:
                    return {
                               'message': f"'{args[var1]}' is not a valid input for {var1}"
                           }, 404
            else:
            # reading answers
                return {
                               'message': f"'{args[var2]}' is not a valid input for {var2}"
                           }, 404
        else:
            return {
                               'message': f"'{args['_id']}' is not a valid ID, please make sure it is 24 characters long"
                           }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', required=True)
        args = parser.parse_args()

        # reading csv file
        all_documents = collection.find()
        list_document = list(all_documents)

        if collection.find_one({'_id': str(args['_id'])}):
            # remove data entry
            collection.delete_one({'_id': str(args['_id'])})

            # reading answers
            return self.get(), 200

        else:
            # if the id does not exist
            return {
                       'message': f"'{args['_id']}' user not found"
                   }, 404

    def check_user_input(self, user_input, classification):
        try:
            if int(user_input):
                if 15 < int(user_input) < 90:
                    return "number"
        except:
            if str(user_input) == 'male' or str(user_input) == 'female':
                return "string"
