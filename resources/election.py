from flask_restful import Resource
from common.dataLoader.dataLoader import data
from conf import CONF

class ElectionList(Resource):
    def get(self):
        return {
            'data':{
                e_type:[
                    {
                        'year':e.year, 
                        'link': CONF['uri_prefix']+'/{}Election/{}/regions'.format(e_type, e.year)
                    } for e in e_collection.values()
                ] for e_type, e_collection in data.items()
            }
        }