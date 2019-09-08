import csv
import os
import re
from common.model.financeData import Record, RecordCollection, PersonalFinanceData


def loadFinanceSummary(root_folder):
    finance_folder_path = '{}/finance_data'.format(root_folder)
    try: 
        files = os.listdir(finance_folder_path)

        for f in files:
            fullpath = os.path.join(finance_folder_path, f)
            if os.path.isdir(fullpath):
                continue

            if f == 'summary.csv':
                return loadSummaryF1(root_folder)
            elif f == 'summary_f2.csv':
                return loadSummaryF2(root_folder)
    except:
        return {}
        

def loadSummaryF1(root_folder):
    data = {}
    income_category = None
    outcome_category = None
    try:
        with open('{}/finance_data/summary.csv'.format(root_folder), 'r') as summary_file:
            reader = csv.reader(summary_file)
            for line in reader:
                try:
                    _ = int(float(line[0]))
                except ValueError:
                    income_category = line[4:10]
                    outcome_category = line[14:24]
                    continue

                name = line[1]
                try:
                    income_list = [int(float(v)) for v in line[4:10]]
                    outcome_list = [int(float(v)) for v in line[14:24]]
                except:
                    continue

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


def isValidElectionType(root_folder_name, election_type):
    if root_folder_name == 'mayor2018':
        if election_type == '107年直轄市市長選舉' or election_type == '107年縣(市)長選舉':
            return True
    elif root_folder_name == 'council2018':
        if election_type == '107年直轄市議員選舉' or election_type == '107年縣(市)議員選舉':
            return True

    return False


def loadSummaryF2(root_folder):
    root_folder_name = root_folder.split('/')[-1]
    data = {}
    income_category = None
    outcome_category = None
    try:
        with open('{}/finance_data/summary_f2.csv'.format(root_folder), 'r') as summary_file:
            reader = csv.reader(summary_file)
            for line in reader:
                try:
                    _ = int(float(line[1]))
                except ValueError:
                    income_category = line[5:11]
                    outcome_category = line[15:25]
                    continue

                election_type = line[3]
                if not isValidElectionType(root_folder_name, election_type):
                    continue

                # region = line[0]
                name = line[2]
                try:
                    income_list = [int(float(v)) for v in line[5:11]]
                    outcome_list = [int(float(v)) for v in line[15:25]]
                except:
                    continue

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
