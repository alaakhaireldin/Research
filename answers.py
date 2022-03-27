from flask_restful import Resource, reqparse
from pymongo import *

client = MongoClient('mongodb+srv://PythonApp:4X0LUM8zjS7Q@researchcluster.usrji.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.research
collection = db.answers


class Answers(Resource):

    def get(self):
        all_documents = collection.find()
        list_document = list(all_documents)
        return {'data': list_document}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_id', required=False)
        parser.add_argument('gender', required=False)
        parser.add_argument('age', required=False)

        args = parser.parse_args()

        # creating new document
        new_data = {
            '_id': args['_id'],
            'gender': args['gender'],
            'age': args['age']
        }
        # adding new document
        collection.update_one(new_data, {'$set': new_data}, upsert=True)

        # reading answers
        return self.get(), 200

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
