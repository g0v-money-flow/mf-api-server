from common.dataLoader.tenderService import TenderService
from common.dataLoader.dataLoader import data

if __name__ == '__main__':
    storage_file = 'common/dataSource/rawData/tenderRepository'
    tender_service = TenderService(storage_file)

    # for category in data.values():
    #     for election in category.values():
    #         for candidate in election.get_candidate_list():
    #             if candidate.finance_data is not None:
    #                 finance = candidate.finance_data
    #                 if '營利事業捐贈收入' in finance.income_records.record_set:
    #                     for record in finance.income_records.record_set['營利事業捐贈收入']:
    #                         tender_service.addTrackingCompany(record.record_obj)
                        

    # company = '新橋聯合股份有限公司'
    company = '趨勢民意調查股份有限公司'

    tender_service.addTrackingCompany(company)
    tender_service.trySyncRemoteData()

    data = tender_service.getCompanyData(company)
    if data is not None:
        for record in data:
            print(record['title'], record['date'])
    