#!/usr/local/bin/python3
import csv


class Record:
    def __init__(self, date, record_type, record_obj, id_number, address, amount):
        self.date = date
        self.record_type = record_type
        self.record_obj = record_obj
        self.id_number = id_number
        self.address = address
        self.amount = amount


class RecordCollection:
    def __init__(self):
        self.record_set = {}
        self.val_sum_set = {}
        self.val_sum = 0

    def addRecord(self, record):
        record_type = record.record_type

        if record_type not in self.record_set:
            self.record_set[record_type] = []
        self.record_set[record_type].append(record)

        if record_type not in self.val_sum_set:
            self.val_sum_set[record_type] = 0
        self.val_sum_set[record_type] += record.amount
        self.val_sum += record.amount

    def getRecords(self):
        return {
            r_type:{
                'sum': self.val_sum_set[r_type],
                'records':[
                    {
                        'object': r.record_obj,
                        'amount': r.amount
                    } for r in records]
            }
        for r_type, records in self.record_set.items()}

    def getValueSumByType(self, record_type):
        if record_type not in self.val_sum_set:
            return 0
        else:
            return self.val_sum_set[record_type]

    def getValueSum(self):
        return self.val_sum


class PersonalFinanceData:
    def __init__(self):
        self.income_records = RecordCollection()
        self.outcome_records = RecordCollection()

    def addIncomeRecord(self, record):
        self.income_records.addRecord(record)

    def addOutcomeRecord(self, record):
        self.outcome_records.addRecord(record)

    def __str__(self):
        return 'income:{}, outcome:{}'.format(self.income_records.getValueSum(), self.outcome_records.getValueSum())


def getFinanceData(name):
    finance_data = PersonalFinanceData()
    with open('common/dataSource/rawData/legislator2016/finance_data/{}.csv'.format(name), 'r') as base_file:
        reader = csv.reader(base_file)
        for line in reader:
            try:
                _ = int(line[0])
            except ValueError:
                continue

            date = line[1]
            record_type = line[2]
            record_obj = line[3]
            id_number = line[4]
            income = line[5]
            outcome = line[6]
            address = line[7]

            if income:
                value = int(income.replace(',', ''))
                t = Record(date, record_type, record_obj,
                           id_number, address, value)
                finance_data.addIncomeRecord(t)
            else:
                value = int(outcome.replace(',', ''))
                t = Record(date, record_type, record_obj,
                           id_number, address, value)
                finance_data.addOutcomeRecord(t)

    return finance_data


if __name__ == '__main__':
    data = getFinanceData('黃秀芳')
    for k in data.outcome_records.record_set.keys():
        print(k)
