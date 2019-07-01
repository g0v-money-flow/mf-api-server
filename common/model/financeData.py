class Record:
    def __init__(self, date, record_type, record_obj, id_number, address, amount):
        self.date = date
        self.record_type = record_type
        self.record_obj = record_obj  # ex. company name or person name
        self.id_number = id_number
        self.address = address
        self.amount = amount


class RecordCollection:
    def __init__(self):
        self.record_set = {}
        self.item_count_set = {}
        self.val_sum_set = {}
        self.val_sum = 0

    def setSummary(self, summary):
        for name, amount in summary.items():
            self.val_sum_set[name] = amount
            self.item_count_set[name] = 0
            self.val_sum += amount

    def addRecord(self, record, skip_finance_type=[]):
        record_type = record.record_type

        if record_type not in skip_finance_type:
            if record_type not in self.record_set:
                self.record_set[record_type] = []
            self.record_set[record_type].append(record)

        if record_type not in self.item_count_set:
            self.item_count_set[record_type] = 1
        else:
            self.item_count_set[record_type] += 1

        if record_type not in self.val_sum_set:
            self.val_sum_set[record_type] = 0
        self.val_sum_set[record_type] += record.amount
        self.val_sum += record.amount

    def getRecords(self):
        result = {
            r_type: {
                'sum': self.val_sum_set[r_type],
                'records': [
                    {
                        'object': r.record_obj,
                        'amount': r.amount
                    } for r in records]
            } for r_type, records in self.record_set.items()
        }

        for r_type, amount in self.val_sum_set.items():
            if r_type not in result:
                item_count = self.item_count_set[r_type]
                average = amount/item_count if amount > 0 else 0
                result[r_type] = {
                    'sum': amount,
                    'records': [{
                        'object': '共{}筆,平均每筆{}元'.format(item_count, average),
                        'amount': amount
                    }]
                }
        return result

    def getValueSumByType(self, record_type):
        if record_type not in self.val_sum_set:
            return 0
        else:
            return self.val_sum_set[record_type]

    def getValueSum(self):
        return self.val_sum

    @property
    def total(self):
        return self.val_sum

    @property
    def items(self):
        return [{'name': k, 'amount': v} for k, v in self.val_sum_set.items()]


class PersonalFinanceData:
    def __init__(self):
        self.income_records = RecordCollection()
        self.outcome_records = RecordCollection()

    def addIncomeRecord(self, record, skip_finance_type=[]):
        self.income_records.addRecord(record, skip_finance_type)

    def addOutcomeRecord(self, record, skip_finance_type=[]):
        self.outcome_records.addRecord(record, skip_finance_type)

    # when we don't have finance detail record. Use it to set summary
    def setIncomeSummary(self, summary):
        self.income_records.setSummary(summary)

    # when we don't have finance detail record. Use it to set summary
    def setOutcomeSummary(self, summary):
        self.outcome_records.setSummary(summary)
