import csv
from common.model.financeData import Record, RecordCollection, PersonalFinanceData

def loadFinanceSummary(root_folder):
    data = {}
    income_category = None
    outcome_category = None
    try:
        with open('{}/finance_data/summary.csv'.format(root_folder), 'r') as summary_file:
            reader = csv.reader(summary_file)
            for line in reader:
                try:
                    _ = int(line[0])
                except ValueError:
                    income_category = line[4:10]
                    outcome_category = line[14:24]
                    continue

                name = line[1]
                income_list = [int(v) for v in line[4:10]]
                outcome_list = [int(v) for v in line[14:24]]

                person_data = PersonalFinanceData()
                person_data.setIncomeSummary(
                    {
                        income_category[idx]: income_list[idx] for idx in range(len(income_list))
                    }
                )
                person_data.setOutcomeSummary(
                    {
                        outcome_category[idx]: outcome_list[idx] for idx in range(len(outcome_list))
                    }
                )
                data[name] = person_data
    finally:
        return data


def getFinanceData(root_folder, name, skip_finance_type=[]):
    finance_data = PersonalFinanceData()

    try:
        with open('{}/finance_data/{}.csv'.format(root_folder, name), 'r') as base_file:
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
                    finance_data.addIncomeRecord(t, skip_finance_type)
                else:
                    value = int(outcome.replace(',', ''))
                    t = Record(date, record_type, record_obj,
                               id_number, address, value)
                    finance_data.addOutcomeRecord(t, skip_finance_type)
        finance_data.executeDataPostProcessing()
        return finance_data

    except FileNotFoundError:
        return None

