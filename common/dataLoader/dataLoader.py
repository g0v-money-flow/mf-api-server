import csv
import re
import os
from common.model.region import Region
from common.model.party import Party
from common.model.person import Person
from common.model.candidate import Candidate
from common.model.election import Election
from common.dataLoader import financeDataLoader
from common.dataLoader.dataDiscover import findAllData


def get_all_election():
    res = []
    for category in data.values():
        for election in category.values():
            res.append(election)
    return res


def get_election(e_type, e_year):
    if e_type not in data:
        return None

    if e_year not in data[e_type]:
        return None

    return data[e_type][e_year]


def get_regions(election):
    return [{
        'name': region_name,
        'constituencies': region_obj
    } for region_name, region_obj in election.city_db.items()]


SKIP_FINANCE_CATEGORY = [
    '個人捐贈收入',
    '匿名捐贈',
    '其他收入',
    '雜支支出',
    '交通旅運支出',
    '返還支出',
    '繳庫支出'
]


def load_data(source):
    root_folder = source['root_folder']
    base_file = source['base_file']
    party_file = source['party_file']
    cand_file = source['cand_file']
    tks_file = source['tks_file']
    election_type = source['name']
    election_year = int(source['year'])
    skip_finance_type = SKIP_FINANCE_CATEGORY

    election = Election(election_type, election_year)
    with open(base_file, 'r') as base_file:
        reader = csv.reader(base_file)
        for line in reader:
            region_code = "-".join(line[0:5])
            name = line[5]

            city = None
            spt = name.find('第')
            if spt != -1:
                city_name = name[:spt]
                region_name = name[spt:]
            else:
                city_name = name
                region_name = name

            if city_name not in election.city_db:
                election.city_db[city_name] = {}
            city = election.city_db[city_name]
            city[region_code] = {
                'name': region_name,
                'id': region_code
            }

            region = Region(region_code, name, city)
            election.region_db[region_code] = region

            if 'instance' not in city[region_code]:
                city[region_code]['instance'] = region

    with open(party_file, 'r') as party_file:
        reader = csv.reader(party_file)
        for line in reader:
            node = {}
            node['party_num'] = line[0]
            node['party_name'] = line[1]

            election.party_db[node['party_num']] = Party(node['party_name'])

    with open(cand_file, 'r') as cand_file:
        vice_list = []
        reader = csv.reader(cand_file)
        for line in reader:
            if line[15] == 'Y':
                # this line is vice candidate
                vice_list.append(line)
                continue

            node = {}
            region_code = "-".join(line[0:5])
            if region_code in election.region_db:
                region = election.region_db[region_code]
            else:
                # there may be only one constituency. so the elbase.csv can't match candidate info 
                region_code = region_code[:7] + '00' +region_code[9:]
                region = election.region_db[region_code]

            # the number only be used in region.
            node['num'] = line[5]
            node['person'] = Person(line[6])
            node['party'] = election.party_db[line[7]]
            if line[14] == '*':
                node['elected'] = True
            else:
                node['elected'] = False

            candidate = Candidate(
                election, region, node['person'], node['party'], node['elected'])
            region.put_candidate(node['num'], candidate)
            election.cand_db[candidate.id] = candidate

        for line in vice_list:
            node = {}
            node['num'] = line[5]
            node['person'] = Person(line[6])
            region_code = "-".join(line[0:5])
            if region_code == '00-000-01-000-0000':
                # fix db elcand_P1.csv format error
                region_code = '00-000-00-000-0000'

            region = election.region_db[region_code]
            candidate = region.get_candidate(node['num'])
            candidate.set_vice_candidate(node['person'])

    with open(tks_file, 'r') as ticket_file:
        reader = csv.reader(ticket_file)
        for line in reader:
            node = {}

            # == the raw data may have issue the region code has format error ==
            # == try two case to fix it
            region_code1 = "-".join(line[0:5])
            line[2] = '01'
            region_code2 = '-'.join(line[0:5])

            region = None
            for code in [region_code1, region_code2]:
                if code in election.region_db:
                    region = election.region_db[code]
                    break
            # =============================
            if region is None:
                continue

            node['num'] = line[6]
            node['num_of_vote'] = line[7]
            node['rate_of_vote'] = line[8]

            candidate = region.get_candidate(node['num'])
            if candidate is not None:
                candidate.set_result(node['num_of_vote'], node['rate_of_vote'])

    finance_summary = financeDataLoader.loadFinanceSummary(root_folder)
    for region in election.region_db.values():
        for _, cand in region.candidates.items():
            city_name = None
            # get city_name
            for k, v in election.city_db.items():
                if v == region.city:
                    city_name = k
                    break

            cand_name = cand.person.name
            for name in [
                '{}-{}'.format(city_name, cand_name), # filename include region name
                cand_name, # filename is candidate name only
                '{}-{}'.format(city_name, re.split("[a-zA-Z]+", cand_name)[0]), # filename include region name, and candidate name excludes english
                re.split("[a-zA-Z]+", cand_name)[0]  # candidate name only and candidate name excludes english
            ]:
                data = financeDataLoader.getFinanceData(
                    root_folder, name, skip_finance_type)
                if data is not None:
                    cand.set_finance_data(data)
                    break
                elif finance_summary and name in finance_summary:
                    cand.set_finance_data(finance_summary[name])
                    break

    # clean invalid region
    delete_region = [region for region in election.region_db.values() if len(
        region.candidates) == 0]
    for region in delete_region:
        code = region.region_code
        del region.city[code]
        del election.region_db[code]

    # clean invalid city
    delete_city = [id for id, city in election.city_db.items()
                   if len(city) == 0]
    for id in delete_city:
        del election.city_db[id]

    return election


def bindSpecialRegion(election_type, special_attr, chinese_name):
    # for example: bind legislatorMountain to legislator as a independent consituency
    CAT_NAME = chinese_name
    CAT_KEY = '{}{}'.format(election_type, special_attr.capitalize())

    if CAT_KEY not in data:
        return

    for year, election in data[CAT_KEY].items():
        if year in data[election_type]:
            parentElection = data[election_type][year]
            childElection = election     # Montain legislator

            for _, city in childElection.city_db.items():
                # only one city
                parentElection.city_db[CAT_NAME] = city

            for region_code, region in childElection.region_db.items():
                # only one region
                parentElection.region_db[CAT_KEY] = region
                # replace region code with CAT_NAME
                parentElection.city_db[CAT_NAME][CAT_KEY] = parentElection.city_db[CAT_NAME][region_code]
                del parentElection.city_db[CAT_NAME][region_code]

            for cand in parentElection.region_db[CAT_KEY].candidates.values():
                parentElection.cand_db[cand.id] = cand
                cand.election = parentElection

    del data[CAT_KEY]


def bindSpecialConsituency(election_type, special_attr, chinese_name):
    # for example: bind legislatorMountain to legislator as a independent consituency
    CAT_KEY = '{}{}'.format(election_type, special_attr.capitalize())

    if CAT_KEY not in data:
        return

    for year, election in data[CAT_KEY].items():
        if year in data[election_type]:
            parentElection = data[election_type][year]
            childElection = election     # Montain council

            for city_name, city in childElection.city_db.items():
                for region_code, region in city.items():
                    parentElection.city_db[city_name][region_code] = region
                    region['name'] = region['name'] + '(' + chinese_name + ')'
                    region['instance'].name = region['name']

            for _, region in childElection.region_db.items():
                for cand in region.candidates.values():
                    parentElection.cand_db[cand.id] = cand
                    cand.election = parentElection

    del data[CAT_KEY]


data_sources = findAllData()

data = {}
for source in data_sources:
    if source['name'] not in data:
        data[source['name']] = {}
    data[source['name']][source['year']] = load_data(source)

bindSpecialRegion('legislator', 'mountain', '山地立委')
bindSpecialRegion('legislator', 'land', '平地立委')
bindSpecialConsituency('council', 'mountain', '山地原住民')
bindSpecialConsituency('council', 'land', '平地原住民')
