import threading
import time
from common.dataLoader.tenderService import TenderService
from common.dataLoader.dataLoader import data

class TenderServiceRunner():
    g_tender_runner = None

    def __init__(self, tender_file):
        self.tender_service = TenderService(tender_file)
        self.stop = False
        self.auto_sync_thread = None

    def getTenderService(self):
        return self.tender_service

    def autoFetchTenderData(self):
        # time.sleep(60)
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
                        for company_name in finance.income_records.company_set:
                            self.tender_service.addTrackingCompany(company_name)

        self.tender_service.trySyncRemoteData()

    def startAutoSync(self):
        if self.auto_sync_thread is None:
            self.auto_sync_thread = threading.Thread(target = self.autoFetchTenderData)
            self.auto_sync_thread.start()


    def stopAutoSync(self):
        self.stop = True


def initTenderService(tender_file):
    if TenderServiceRunner.g_tender_runner is None:
        TenderServiceRunner.g_tender_runner = TenderServiceRunner(tender_file)
        TenderServiceRunner.g_tender_runner.startAutoSync()

def getTenderService():
    return TenderServiceRunner.g_tender_runner.getTenderService()
