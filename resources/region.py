from flask_restful import Resource
from flask import abort
from common.data_loader import data

class RegionList(Resource):
    def get(self, electionName, year):
        e_type = electionName[:-8]
        if e_type not in data:
            abort(404)
        
        if str(year) not in data[e_type]:
            abort(404)

        return {
            'data':{
                'regions':[
                    {
                        'name':'Taipei',
                        'link':'link'
                    },
                    {
                        'name':'Hsinchu',
                        'link':'link'
                    }
                ]
            }
        }