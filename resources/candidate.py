from flask_restful import Resource
from flask import abort
from common.data_loader import data

class Candidate(Resource):
    def get(self, electionName, year, id):
        e_type = electionName[:-8]
        e_year = str(year)
        if e_type not in data:
            abort(404)
        
        if e_year not in data[e_type]:
            abort(404)

        if id not in data[e_type][e_year].cand_db:
            abort(404)
        
        target = data[e_type][e_year].cand_db[id]

        return {
             'data': {
                'id': target.id,
                'party': target.party.name,
                'name': target.person.name,
                'is_elected': target.is_elected,
                'num_of_vote': target.num_of_vote,
                'rate_of_vote': target.rate_of_vote,
                'finance_data': Candidate._gen_finance_detail_record(target),
            }
        }

    @classmethod
    def _gen_finance_detail_record(cls, candidate):
        if candidate.finance_data is None:
            return None
        else:
            return {
                'income': candidate.finance_data.income_records.getRecords(),
                'outcome': candidate.finance_data.outcome_records.getRecords()
            }
