from flask import Flask
from flask_restful import Api, Resource
from resources.election import ElectionList

app = Flask(__name__)
api = Api(app)

api.add_resource(ElectionList, '/elections')

if __name__ == '__main__':
    app.run(debug=True)