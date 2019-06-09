from flask import Flask
from flask_restful import Api, Resource
from resources.election import ElectionList
from resources.region import RegionList
from resources.constitution import Constitution
from resources.candidate import Candidate

app = Flask(__name__)
api = Api(app)

api.add_resource(ElectionList, '/elections')
api.add_resource(RegionList, '/<string:electionName>/<int:year>/regions')
api.add_resource(Constitution, '/<string:electionName>/<int:year>/constitutions/<string:id>')
api.add_resource(Candidate, '/<string:electionName>/<int:year>/candidates/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)