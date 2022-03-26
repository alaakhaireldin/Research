import ast

from flask_restful import Resource, reqparse
import pandas as pd

class Answers(Resource):

    def get(self):
        data = pd.read_csv('answers.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('_id', required=False)
        parser.add_argument('gender', required=False)
        parser.add_argument('age', required=False)

        args = parser.parse_args()

#         creating new dataframe
        new_data = pd.DataFrame({
            '_id': args['_id'],
            'gender': args['gender'],
            'age': args['age'],
            'locations':[[]]
        },
        index=[0])

#       reading answers csv
        data = pd.read_csv('answers.csv')

        if args['_id'] in list(data['_id']):
            return {
                'message': f"'{args['_id']}' already exists."
            }, 401
        else:
#           add the newly provided data
            data = data.append(new_data, ignore_index=True)

#           save back to csv
            data.to_csv('answers.csv', index=False)

            return {'data':data.to_dict()}, 200

    def put(self):
#         reading csv file
        parser = reqparse.RequestParser()
        parser.add_argument('_id', required=False)
        parser.add_argument('location', required=False)
        args = parser.parse_args()

#         reading csv file
        data = pd.read_csv('answers.csv')

        if args['_id'] in list(data['_id']):
#           evaluate strings of lists to lists

            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
#           select the users by id
            user_data = data[data['_id'] == args['_id']]

#           updating user's location
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

#           save back to csv
            data.to_csv('answer.csv', index=False)

#           return the data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
#             if the id does not exist
            return {
                'message': f"'{args['_id']}' user not found"
            }, 404

    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument('_id', required=False)
        args = parser.parse_args()

        #         reading csv file
        data = pd.read_csv('answers.csv')

        if args['_id'] in list(data['_id']):
            #           remove data entry
            data = data[data['_id'] != args['_id']]

            #           save back to csv
            data.to_csv('answer.csv', index=False)

            #           return the data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            #             if the id does not exist
            return {
                       'message': f"'{args['_id']}' user not found"
                   }, 404



class Locations(Resource):
    pass
