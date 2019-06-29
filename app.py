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
from common.dataLoader.tenderService import TenderService
from tenderServiceRunner import TenderServiceRunner

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(ElectionList, '/elections')
api.add_resource(RegionList, '/<string:electionName>/<int:year>/regions')
api.add_resource(Constituency, '/<string:electionName>/<int:year>/constituencies/<string:id>')
api.add_resource(Candidate, '/<string:electionName>/<int:year>/candidates/<int:id>')

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema = Schema(Query), graphiql = True))

if __name__ == '__main__':
    # TENDER_DATA_FILE = 'common/dataSource/rawData/tenderRepository'
    # tender_service = TenderService(TENDER_DATA_FILE)
    # tender_runner = TenderServiceRunner(tender_service)
    # tender_runner.startAutoSync()

    app.run(debug=True)

    # tender_runner.stopAutoSync()