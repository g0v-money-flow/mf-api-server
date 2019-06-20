import csv
from common.model.region import Region
from common.model.party import Party
from common.model.person import Person 
from common.model.candidate import Candidate
from common.model.election import Election
from common.dataSource import finance_data


def get_election(e_type, e_year):
    if e_type not in data:
        return None
        
    if e_year not in data[e_type]:
        return None
    
    return data[e_type][e_year]

def get_regions(election):
    return [{
        'name':region_name,
        'constituencies': region_obj
    } for region_name, region_obj in election.city_db.items()]

def get_candidate(name):
    for etype in data.values():
        for e in etype.values():
            for cand in e.cand_db.values():
                if cand.name == name:
                    return cand
    return None
    
def load_data():
    election = Election()

    with open('common/dataSource/rawData/legislator2016/elbase_T1.csv', 'r') as base_file:
        reader = csv.reader(base_file)
        for line in reader:
            region_code = "-".join(line[0:5])
            name = line[5]

            city = None
            spt = name.find('第')
            if spt != -1:
                city_name = name[:spt]
                region_name = name[spt:]

                if city_name not in election.city_db:
                    election.city_db[city_name] = {}
                city = election.city_db[city_name]
                city[region_code]={
                    'name': region_name,
                    'id': region_code
                }

            region = Region(region_code, name, city)
            election.region_db[region_code] = region
            
            if city is not None:
                city[region_code]['instance'] = region

    with open('common/dataSource/rawData/legislator2016/elpaty.csv', 'r') as party_file:
        reader = csv.reader(party_file)
        for line in reader:
            node = {}
            node['party_num'] = line[0]
            node['party_name'] = line[1]

            election.party_db[node['party_num']] = Party(node['party_name'])

    with open('common/dataSource/rawData/legislator2016/elcand_T1.csv', 'r') as cand_file:
        vice_list = []
        reader = csv.reader(cand_file)
        for line in reader:
            if line[15] == 'Y':
                vice_list.append(line)
                continue

            node = {}
            region_code = "-".join(line[0:5])
            if region_code == '00-000-01-000-0000':
                #fix db elcand_P1.csv format error
                region_code = '00-000-00-000-0000'
            region = election.region_db[region_code]

            #the number only be used in region.
            node['num'] = line[5]
            node['person'] = Person(line[6])
            node['party'] = election.party_db[line[7]]
            if line[14] == '*':
                node['elected'] = True
            else:
                node['elected'] = False

            candidate = Candidate(region, node['person'], node['party'], node['elected'])
            region.put_candidate(node['num'], candidate)
            election.cand_db[candidate.id] = candidate
            
        for line in vice_list:        
            node = {}
            node['num'] = line[5]
            node['person'] = Person(line[6])
            region_code = "-".join(line[0:5])
            if region_code == '00-000-01-000-0000':
                #fix db elcand_P1.csv format error
                region_code = '00-000-00-000-0000'
                
            region = election.region_db[region_code]
            candidate = region.get_candidate(node['num'])
            candidate.set_vice_candidate(node['person'])

    with open('common/dataSource/rawData/legislator2016/elctks_T1.csv', 'r') as ticket_file:
        reader = csv.reader(ticket_file)
        for line in reader:
            node = {}
            region_code = "-".join(line[0:5])
            if region_code not in election.region_db:
                continue
            region = election.region_db[region_code]
            node['num'] = line[6]
            node['num_of_vote'] = line[7]
            node['rate_of_vote'] = line[8]

            candidate = region.get_candidate(node['num'])
            if candidate is not None:
                candidate.set_result(node['num_of_vote'], node['rate_of_vote'])

    for region in election.region_db.values():
        for num, cand in region.candidates.items():
            cand_name = cand.person.name
            try:
                data = finance_data.getFinanceData(cand_name)
                cand.set_finance_data(data)
            except FileNotFoundError:
                pass

    return election

data = {
    'legislator': {
        '2016': load_data()
    }
}