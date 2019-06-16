from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene import Schema
from resources.election import ElectionList
from resources.region import RegionList
from resources.constitution import Constitution
from resources.candidate import Candidate
from graphql_api.schema import Query

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(ElectionList, '/elections')
api.add_resource(RegionList, '/<string:electionName>/<int:year>/regions')
api.add_resource(Constitution, '/<string:electionName>/<int:year>/constitutions/<string:id>')
api.add_resource(Candidate, '/<string:electionName>/<int:year>/candidates/<int:id>')

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema = Schema(Query), graphiql = True))

if __name__ == '__main__':
    app.run(debug=True)