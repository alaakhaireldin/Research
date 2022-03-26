from flask_restful import Resource, reqparse
import pandas as pd

class Answers(Resource):

    def get(self):
        data = pd.read_csv('answers.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=False)
        parser.add_argument('gender', required=False)
        parser.add_argument('age', required=False)

        args = parser.parse_args()

#         creating new dataframe
        new_data = pd.DataFrame({
            '_id': args['userId'],
            'gender': args['gender'],
            'age': args['age']
        },
        index=[0])

#       reading answers csv
        data = pd.read_csv('answers.csv')

#       add the newly provided data
        data = data.append(new_data, ignore_index=True)

#       save back to csv
        data.to_csv('answers.csv', index=False)

        return {'data':data.to_dict()}, 200




class Locations(Resource):
    pass
