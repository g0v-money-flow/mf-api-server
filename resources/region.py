from flask_restful import Resource
from flask import abort
from common.data_loader import data, get_election, get_regions
from conf import CONF

class RegionList(Resource):
    def get(self, electionName, year):
        e_type = electionName[:-8]
        e_year = str(year)
        election = get_election(e_type, e_year)

        if election is None:
            abort(404)

        return {
            'data':{
                'regions':[
                    {
                        'name':region['name'],
                        'link':CONF['uri_prefix']+'/{}Election/{}/constituencies/{}'.format(
                            e_type, e_year, RegionList.__getFirstConstituency(region['constituencies'])
                        )
                    } for region in get_regions(election)
                ]
            }
        }

    @classmethod
    def __getFirstConstituency(cls, region_obj):
        return sorted(region_obj.keys())[0]