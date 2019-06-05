from flask_restful import Resource
from common.data_loader import data

class ElectionList(Resource):
    def get(self):
        return {
            'data':{
                e_type:[
                    {
                        'year':e.year, 
                        'link':'/{}Election/{}/regions'.format(e_type, e.year)
                    } for e in e_collection.values()
                ] for e_type, e_collection in data.items()
            }
        }