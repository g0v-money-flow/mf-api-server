import asyncio
from datetime import datetime, timedelta
import time
import pytz
from common.dataLoader import tenderLoader

class TenderService():
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.repository = tenderLoader.loadTenderRepository(self.storage_file)
        self.tracking_companies = {}
        if 'last_update' in self.repository:
            self.remote_source_last_update = datetime.fromisoformat(
                self.repository['last_update'])
        else:
            self.remote_source_last_update = None

    def addTrackingCompany(self, company):
        if company in self.tracking_companies:
            return

        self.tracking_companies[company] = True
        if self.remote_source_last_update is not None:
            self.loadCompany(company)

    def trySyncRemoteData(self):
        if len(self.tracking_companies) == 0:
            return

        latest_update = tenderLoader.getLatestUpdateTime()
        if latest_update is None:
            return

        if self.remote_source_last_update:
            target_date = self.remote_source_last_update + timedelta(days=1)
        else:
            # begin_date = datetime(2010, 1, 4, tzinfo = pytz.timezone('Asia/Taipei'))
            target_date = datetime(2019, 6, 10, tzinfo = pytz.timezone('Asia/Taipei'))

        if latest_update < target_date:
            return

        print('start to sync remote data')
        while target_date <= latest_update:
            print('fetch data {}'.format(target_date.strftime('%Y%m%d')))
            data = tenderLoader.fetchTendersByDate(target_date)

            for company_name in self.tracking_companies.keys():
                self.__mergeDataToRepositoryByCompanyName(company_name, data)
                time.sleep(5)

            self.remote_source_last_update = target_date
            target_date += timedelta(days=1)
        print('sync finished')

    def loadCompany(self, company_name):
        if self.getCompanyData(company_name) is not None:
            return

        data = tenderLoader.fetchTendersByCompanyName(company_name)
        self.__mergeDataToRepositoryByCompanyName(company_name, data)

    def __mergeDataToRepositoryByCompanyName(self, company_name, data):
        max_date = 0
        for d in data:
            if d['date'] > max_date:
                max_date = d['date']

        if data is not None:
            if company_name in self.repository:
                company = self.repository[company_name]
                last_update = company['max_date']
                for d in data:
                    if company_name in d['winner'] and d['date'] > last_update:
                        company['records'].append(d)
                company['max_date'] = max_date
            else:
                company = {
                    'max_date': max_date,
                    'records': []
                }
                for d in data:
                    if company_name in d['winner']:
                        company['records'].append(d)
                self.repository[company_name] = company
                

    def getCompanyData(self, company_name):
        if company_name in self.repository:
            return self.repository[company_name]['records']
        else:
            return None

    def stop(self):
        if self.remote_source_last_update:
            self.repository['last_update'] = self.remote_source_last_update.isoformat(
            )
        tenderLoader.exportTenderRepository(self.storage_file, self.repository)

