from flask_restful import Resource
from flask import abort
from common.data_loader import data
from conf import CONF

class RegionList(Resource):
    def get(self, electionName, year):
        e_type = electionName[:-8]
        e_year = str(year)
        if e_type not in data:
            abort(404)
        
        if e_year not in data[e_type]:
            abort(404)

        return {
            'data':{
                'regions':[
                    {
                        'name':region_name,
                        'link':CONF['uri_prefix']+'/{}Election/{}/constitutions/{}'.format(e_type, e_year, RegionList.__getFirstConstitution(region_obj))
                    } for region_name, region_obj in data[e_type][e_year].city_db.items()
                ]
            }
        }

    @classmethod
    def __getFirstConstitution(cls, region_obj):
        return sorted(region_obj.keys())[0]