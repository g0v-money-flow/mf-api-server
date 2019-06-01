from flask_restful import Resource
from common.data_loader import data

class ElectionList(Resource):
    def get(self):
        return {
            'legislator':[{'year':e.year, 'link': 'link'} for e in data]
        }