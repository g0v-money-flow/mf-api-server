from flask_restful import Resource
from flask import abort
from common.data_loader import data, get_election
from conf import CONF

class Constitution(Resource):
    def get(self, electionName, year, id):
        e_type = electionName[:-8]
        e_year = str(year)
        election = get_election(e_type, e_year)
        
        if election is None:
            abort(404)
        
        if id not in election.region_db:
            abort(404)
        
        target = election.region_db[id]

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
                        'finance_data': Constitution._gen_finance_data(c),
                        'detail': CONF['uri_prefix'] + '/{}Election/{}/candidates/{}'.format(e_type, e_year, c.id)
                    } for c in target.get_candidates()
                ],
                'constitutions':[{
                    'name': r['name'],
                    'link': CONF['uri_prefix'] + '/{}Election/{}/constitutions/{}'.format(e_type, e_year, r['id'])
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
