import threading
import time
from common.dataLoader.tenderService import TenderService
from common.dataLoader.dataLoader import data

class TenderServiceRunner():
    def __init__(self, tender_service):
        self.tender_service = tender_service
        self.stop = False
        self.auto_sync_thread = None

    def autoFetchTenderData(self):
        print('start tenderServiceRunner')
        while not self.stop:
            self.syncData()
            time.sleep(1800)  # 30 min

    def syncData(self):
        if self.tender_service is None:
            return

        for category in data.values():
            for election in category.values():
                for candidate in election.get_candidate_list():
                    if candidate.finance_data is not None:
                        finance = candidate.finance_data
                        if '營利事業捐贈收入' in finance.income_records.record_set:
                            for record in finance.income_records.record_set['營利事業捐贈收入']:
                                self.tender_service.addTrackingCompany(
                                    record.record_obj)

        self.tender_service.trySyncRemoteData()

    def startAutoSync(self):
        if self.auto_sync_thread is None:
            self.auto_sync_thread = threading.Thread(target = self.autoFetchTenderData)
            self.auto_sync_thread.start()


    def stopAutoSync(self):
        self.stop = True
