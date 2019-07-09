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
        self.company_set = set()
        self.record_list = []
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

        if record_type == '營利事業捐贈收入':
            self.company_set.add(record.record_obj)

        if record_type not in skip_finance_type:
            self.record_list.append(record)

        if record_type not in self.item_count_set:
            self.item_count_set[record_type] = 1
        else:
            self.item_count_set[record_type] += 1

        if record_type not in self.val_sum_set:
            self.val_sum_set[record_type] = 0
        self.val_sum_set[record_type] += record.amount
        self.val_sum += record.amount

    def filterOutTop100Record(self):
        def getAmount(r):
            return r['amount']

        organize_dict = {}
        for record in self.record_list:
            if record.record_obj in organize_dict:
                organize_dict[record.record_obj] += record.amount
            else:
                organize_dict[record.record_obj] = record.amount

        amount_list = [
            {'obj': obj, 'amount': amount}
            for obj, amount in organize_dict.items()
        ]
        amount_list.sort(key=getAmount, reverse=True)
        amount_list = amount_list[:100]

        top100_org = set()
        for amount_info in amount_list:
            top100_org.add(amount_info['obj'])

        total_by_type = {}
        for r in self.record_list:
            if r.record_obj in top100_org:
                if r.record_type not in total_by_type:
                    total_by_type[r.record_type] = {}

                if r.record_obj in total_by_type[r.record_type]:
                    total_by_type[r.record_type][r.record_obj] += r.amount
                else:
                    total_by_type[r.record_type][r.record_obj] = r.amount

        self.record_list = [
            {
                'obj': organization,
                'type': category,
                'amount': amount
            }
            for category, organizations in total_by_type.items() 
            for organization, amount in organizations.items()
        ]
        self.record_list.sort(key=getAmount, reverse=True)

    def getRecords(self, category_list=[]):
        result = {}
        for category in category_list:
            if category in self.val_sum_set:
                result[category] = {
                    'name': category,
                    'amount': self.val_sum_set[category],
                    'item_count': self.item_count_set[category]
                }
            else:
                result[category] = {
                    'name': category,
                    'amount': 0,
                    'item_count': 0
                }

        result['top100'] = [
            {
                'amount': record['amount'],
                'object': record['obj'],
                'type': record['type']
            }
            for record in self.record_list]

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


class PersonalFinanceData:
    def __init__(self):
        self.income_records = RecordCollection()
        self.outcome_records = RecordCollection()

    def addIncomeRecord(self, record, skip_finance_type=[]):
        self.income_records.addRecord(record, skip_finance_type)

    def addOutcomeRecord(self, record, skip_finance_type=[]):
        self.outcome_records.addRecord(record, skip_finance_type)

    def executeDataPostProcessing(self):
        self.income_records.filterOutTop100Record()
        self.outcome_records.filterOutTop100Record()

    # when we don't have finance detail record. Use it to set summary
    def setIncomeSummary(self, summary):
        self.income_records.setSummary(summary)

    # when we don't have finance detail record. Use it to set summary
    def setOutcomeSummary(self, summary):
        self.outcome_records.setSummary(summary)


INCOME_CATEGORY = ['個人捐贈收入', '營利事業捐贈收入', '政黨捐贈收入', '人民團體捐贈收入', '匿名捐贈', '其他收入']
OUTCOME_CATEGORY = ['人事費用支出', '宣傳支出', '租用宣傳車輛支出', '租用競選辦事處支',
                    '集會支出', '交通旅運支出', '雜支支出', '返還支出', '繳庫支出', '公共關係費用支出']
