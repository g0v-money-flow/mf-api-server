from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene import Schema
from resources.election import ElectionList
from resources.region import RegionList
from resources.constituency import Constituency
from resources.candidate import Candidate
from graphql_api.schema import Query
import tenderServiceRunner

TENDER_DATA_FILE = 'common/dataSource/rawData/tenderRepository'
tenderServiceRunner.initTenderService(TENDER_DATA_FILE)

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(ElectionList, '/elections')
api.add_resource(RegionList, '/<string:electionName>/<int:year>/regions')
api.add_resource(Constituency, '/<string:electionName>/<int:year>/constituencies/<string:id>')
api.add_resource(Candidate, '/<string:electionName>/<int:year>/candidates/<int:id>')

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema = Schema(Query), graphiql = True))
