import threading
import time
from common.dataLoader.tenderService import TenderService
from common.dataLoader.dataLoader import data

stop = False
serviceThread = None


def autoFetchTenderData():
    print('start tenderServiceRunner')
    while not stop:
        syncData()
        time.sleep(1800)  # 30 min


def syncData():
    storage_file = 'common/dataSource/rawData/tenderRepository'
    tender_service = TenderService(storage_file)

    for category in data.values():
        for election in category.values():
            for candidate in election.get_candidate_list():
                if candidate.finance_data is not None:
                    finance = candidate.finance_data
                    if '營利事業捐贈收入' in finance.income_records.record_set:
                        for record in finance.income_records.record_set['營利事業捐贈收入']:
                            tender_service.addTrackingCompany(
                                record.record_obj)

    tender_service.trySyncRemoteData()


def startService():
    if serviceThread is None:
        serviceThread = threading.Thread(target=autoFetchTenderData)
        serviceThread.start()


def stopService():
    stop = True
