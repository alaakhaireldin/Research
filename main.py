from flask import Flask
from flask_restful import Api

from answers import Answers
app = Flask(__name__)
api = Api(app)

api.add_resource(Answers, '/answers')


if __name__ == '__main__':
    app.run()

