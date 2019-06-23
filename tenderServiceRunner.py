from common.dataLoader.tenderService import TenderService
# from common.dataLoader.dataLoader import data

if __name__ == '__main__':
    storage_file = 'common/dataSource/rawData/tenderRepository'
    tender_service = TenderService(storage_file)

    company = '新橋聯合股份有限公司'

    tender_service.addTrackingCompany(company)
    tender_service.trySyncRemoteData()

    for record in tender_service.getCompanyData(company):
        print(record['title'])

    tender_service.stop()