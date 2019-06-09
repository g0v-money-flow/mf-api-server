from flask_restful import Resource
from flask import abort
from common.data_loader import data

class Constitution(Resource):
    def get(self, electionName, year, id):
        e_type = electionName[:-8]
        e_year = str(year)
        if e_type not in data:
            abort(404)
        
        if e_year not in data[e_type]:
            abort(404)

        if id not in data[e_type][e_year].region_db:
            abort(404)
        
        target = data[e_type][e_year].region_db[id]

        return {
            'data':{
                'id': id,
                'name': target.name,
                'candidates':[
                    {
                        'id': c.id,
                        'party': c.party.name,
                        'name': c.person.name,
                        'is_elected': c.is_elected,
                        'num_of_vote': c.num_of_vote,
                        'rate_of_vote': c.rate_of_vote,
                        'finance_data': Constitution._gen_finance_data(c)
                    } for c in target.get_candidates()
                ],
                'constitutions':[{
                    'name': r['name'],
                    'link': '/{}Election/{}/constitutions/{}'.format(e_type, e_year, r['id'])
                } for r in target.city.values() if r['id'] != id]
            }
        }

    @classmethod
    def _gen_finance_data(cls, candidate):
        if candidate.finance_data is None:
            return None
        else:
            return {
                'income': candidate.finance_data.income_records.val_sum_set,
                'outcome': candidate.finance_data.outcome_records.val_sum_set,
            }
