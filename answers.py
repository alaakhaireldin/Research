from flask_restful import Resource, reqparse
from pymongo import *

client = MongoClient('mongodb+srv://PythonApp:4X0LUM8zjS7Q@researchcluster.usrji.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.research
collection = db.answers

var1 = 'gender'
var2 = 'age'
all_variables = [var1, var2]


def validationInput(argument, var_age):
    if len(argument) == 0:
        return f"'you cannot leave the {var_age} field empty"
    if not argument.isnumeric():
        return f"'{argument}' is not a valid input for {var_age}"
    if not 5 < int(argument) < 100:
        return f"'{argument}' is not a valid input for {var_age}, it must be between 5 and 100"
    return None

def validationInputGender(argument, var_gender):
    if len(argument) == 0:
        return f"'you cannot leave the {var_gender} field empty"
    if argument != 'female' or argument != 'male':
        return f" {argument} is not a valid input for {var_gender}, must be 'male' or 'female'"


class Answers(Resource):

    def get(self):
        all_documents = collection.find()
        list_document = list(all_documents)
        # change each element's _id type from 'bson.objectid.ObjectId' to 'str' to be returned to the final json view
        data = []
        for document in list_document:
            document['_id'] = str(document['_id'])
            data.append(document)
        # data = map((self.change_to_string, list_document))
        return {'data': data}, 200





    def post(self):
        parser = reqparse.RequestParser()
        for var in all_variables:
            parser.add_argument(var, required=True)
        args = parser.parse_args()



        # creating new document
        new_data = {}
        for var in all_variables:
            new_data[var] = args[var]

        age_error = validationInput(args[var2], var2)
        gender_error = validationInputGender(args[var1], var1)

        if age_error:
            return {'message': age_error}, 400

        if gender_error:
            return {'message': gender_error}, 400
        # adding new document
        else:
            collection.update_one(new_data, {'$set': new_data}, upsert=True)
            return self.get(), 200


    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(var1, required=True)
        parser.add_argument(var2, required=True)
        args = parser.parse_args()

        if collection.find_one({var1: str(args[var1])}) and collection.find_one({var2: str(args[var2])}):
            # remove data entry
            collection.delete_one({var1: str(args[var1])})
            # reading answers
            return self.get(), 200

        else:
            # if the id does not exist
            return {
                       'message': f"'{args[var1]}', '{args[var2]}' not found"
                   }, 404


