import asyncio
from datetime import datetime, timedelta
import iso8601
import time
import pytz
from common.dataLoader import tenderLoader


class TenderService():
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.repository = tenderLoader.loadTenderRepository(self.storage_file)
        self.tracking_companies = {}
        if 'last_update' in self.repository:
            self.remote_source_last_update = iso8601.parse_date(
                self.repository['last_update'])
        else:
            self.remote_source_last_update = None

    def addTrackingCompany(self, company):
        if company in self.tracking_companies:
            return

        # print('add tracking company', company)
        self.tracking_companies[company] = True

    def trySyncRemoteData(self):
        if len(self.tracking_companies) == 0:
            return

        latest_update = tenderLoader.getLatestUpdateTime()
        # latest_update = datetime(
        # 2018, 8, 30, tzinfo=pytz.timezone('Asia/Taipei'))
        if latest_update is None:
            return

        is_first_fetch = False
        if self.remote_source_last_update:
            target_date = self.remote_source_last_update + timedelta(days=1)
        else:
            self._resetLastUpdateDate()
            target_date = self.remote_source_last_update
            is_first_fetch = True

        print('start to sync remote data')
        nodata_company = [
            company for company in self.tracking_companies.keys() if self.getCompanyData(company) is None
        ]
        if len(nodata_company) > 1200:
            # reset target_date for re-fetching all tender data
            self._resetLastUpdateDate()
            target_date = self.remote_source_last_update
        else:
            for company in nodata_company:
                self.loadCompany(company)

            if is_first_fetch:
                self.remote_source_last_update = latest_update
                target_date = latest_update + timedelta(days=1)

        if latest_update >= target_date:
            while target_date <= latest_update:
                print('fetch data {}'.format(target_date.strftime('%Y%m%d')))
                data = tenderLoader.fetchTendersByDate(target_date)

                for company_name in self.tracking_companies.keys():
                    self.__mergeDataToRepositoryByCompanyName(
                        company_name, data)
                self.remote_source_last_update = target_date
                target_date += timedelta(days=1)
                time.sleep(1)

        self.keepRepository()
        print('sync finished')

    def loadCompany(self, company_name):
        print('try to fetch remote tender records ', company_name)
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
                        detail = tenderLoader.fetchTenderAmountAndDate(
                            company_name, d['tender_api_url'])
                        
                        if detail == None:
                            continue
                        
                        d['decisionDate'] = detail['date']
                        d['amount'] = detail['amount']
                        company['records'].append(d)
                company['max_date'] = max_date
            else:
                company = {
                    'max_date': max_date,
                    'records': []
                }
                for d in data:
                    if company_name in d['winner']:
                        detail = tenderLoader.fetchTenderAmountAndDate(
                            company_name, d['tender_api_url'])
                        if detail == None:
                            continue
                        d['decisionDate'] = detail['date']
                        d['amount'] = detail['amount']
                        company['records'].append(d)
                self.repository[company_name] = company

    def getCompanyData(self, company_name):
        if company_name in self.repository:
            return self.repository[company_name]['records']
        else:
            return None

    def keepRepository(self):
        if self.remote_source_last_update:
            self.repository['last_update'] = self.remote_source_last_update.isoformat(
            )
        tenderLoader.exportTenderRepository(self.storage_file, self.repository)

    def _resetLastUpdateDate(self):
        self.remote_source_last_update = datetime(
            2010, 1, 1, tzinfo=pytz.timezone('Asia/Taipei'))
