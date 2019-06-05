from flask import Flask
from flask_restful import Api, Resource
from resources.election import ElectionList
from resources.region import RegionList

app = Flask(__name__)
api = Api(app)

api.add_resource(ElectionList, '/elections')
api.add_resource(RegionList, '/<string:electionName>/<int:year>/regions')

if __name__ == '__main__':
    app.run(debug=True)