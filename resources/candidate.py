from flask_restful import Resource
from flask import abort
from common.dataLoader.dataLoader import data
import tenderServiceRunner

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
        finance_data = Candidate._gen_finance_detail_record(target)
        if finance_data:
            tenders = Candidate._gen_tender_list(
                finance_data['income']['營利事業捐贈收入']['records']) if '營利事業捐贈收入' in finance_data['income'] else []
        else:
            tenders = []

        result = {
            'data': {
                'id': target.id,
                'party': target.party.name,
                'name': target.person.name,
                'is_elected': target.is_elected,
                'num_of_vote': target.num_of_vote,
                'rate_of_vote': target.rate_of_vote,
                'finance_data': finance_data,
                'tenders': tenders
            }
        }
        if target.vice:
            result['data']['vice_candidate'] = target.vice.name

        return result

    @classmethod
    def _gen_finance_detail_record(cls, candidate):
        if candidate.finance_data is None:
            return None
        else:
            return {
                'income': candidate.finance_data.income_records.getRecords(),
                'outcome': candidate.finance_data.outcome_records.getRecords()
            }

    @classmethod
    def _gen_tender_list(cls, income_records):
        company_set = set()
        for records in income_records:
            company_set.add(records['object'])

        res = []
        for company_name in company_set:
            tenders = tenderServiceRunner.getTenderService().getCompanyData(company_name)
            if tenders is not None:
                res.extend(tenders)
        return res
