#!/usr/local/bin/python3
import csv
from . import finance_data

class Region:
    region_code:str
    name:str
    city:dict

    def __init__(self, code, name, city):
        self.region_code = code
        self.name = name
        self.candidates = {}
        self.city = city
    
    def has_candidate(self):
        return len(self.candidates) > 0

    def put_candidate(self, number, candidate):
        self.candidates[number] = candidate

    def get_candidate(self, number):
        if number in self.candidates:
            return self.candidates[number]
        else:
            return None

    def get_candidates(self):
        return self.candidates.values()

    def get_count_of_candidate(self):
        return len(self.candidates)

    def __str__(self):
        return self.name

    def __dict__(self):
        return self.region_code.__dict__()

class Party:
    name:str
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Person:
    name:str

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Candidate:
    # class member
    id_counter = 0

    # object member
    id:int
    region:Region
    party:Party
    person:Person
    vice:Person
    is_elected:bool
    num_of_vote:int
    rate_of_vote:float
    
    @classmethod
    def generateId(cls):
        cls.id_counter += 1
        tmp = cls.id_counter
        return tmp
    
    def __init__(self, region, person, party, is_elected):
        self.id = Candidate.generateId()
        self.region = region
        self.person = person
        self.party = party
        self.is_elected = is_elected
        self.vice = None
        self.finance_data = None

    def set_vice_candidate(self, person):
        self.vice = person

    def set_result(self, num_of_vote, rate_of_vote):
        self.num_of_vote = num_of_vote
        self.rate_of_vote = rate_of_vote

    def set_finance_data(self, finance_data):
        self.finance_data = finance_data

    def __str__(self):
        if self.vice is None:
            return '{} {}, {}: {}, {}%'.format(self.party, self.person, self.is_elected, self.num_of_vote, self.rate_of_vote)
        else:
            return '{} {}, {}, {}: {}, {}%'.format(self.party, self.person, self.vice, self.is_elected, self.num_of_vote, self.rate_of_vote)

class Election:
    def __init__(self):
        self.year = 2016
        self.city_db = {}
        self.region_db = {}
        self.party_db = {}
        self.cand_db = {}

    def load_data(self):
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

                    if city_name not in self.city_db:
                        self.city_db[city_name] = {}
                    city = self.city_db[city_name]
                    city[region_code]={
                        'name': region_name,
                        'id': region_code
                    }

                self.region_db[region_code] = Region(region_code, name, city)

        with open('common/dataSource/rawData/legislator2016/elpaty.csv', 'r') as party_file:
            reader = csv.reader(party_file)
            for line in reader:
                node = {}
                node['party_num'] = line[0]
                node['party_name'] = line[1]

                self.party_db[node['party_num']] = Party(node['party_name'])

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
                region = self.region_db[region_code]

                #the number only be used in region.
                node['num'] = line[5]
                node['person'] = Person(line[6])
                node['party'] = self.party_db[line[7]]
                if line[14] == '*':
                    node['elected'] = True
                else:
                    node['elected'] = False

                candidate = Candidate(region, node['person'], node['party'], node['elected'])
                region.put_candidate(node['num'], candidate)
                self.cand_db[candidate.id] = candidate
                
            for line in vice_list:        
                node = {}
                node['num'] = line[5]
                node['person'] = Person(line[6])
                region_code = "-".join(line[0:5])
                if region_code == '00-000-01-000-0000':
                    #fix db elcand_P1.csv format error
                    region_code = '00-000-00-000-0000'
                    
                region = self.region_db[region_code]
                candidate = region.get_candidate(node['num'])
                candidate.set_vice_candidate(node['person'])

        with open('common/dataSource/rawData/legislator2016/elctks_T1.csv', 'r') as ticket_file:
            reader = csv.reader(ticket_file)
            for line in reader:
                node = {}
                region_code = "-".join(line[0:5])
                if region_code not in self.region_db:
                    continue
                region = self.region_db[region_code]
                node['num'] = line[6]
                node['num_of_vote'] = line[7]
                node['rate_of_vote'] = line[8]

                candidate = region.get_candidate(node['num'])
                if candidate is not None:
                    candidate.set_result(node['num_of_vote'], node['rate_of_vote'])

        for region in self.region_db.values():
            for num, cand in region.candidates.items():
                cand_name = cand.person.name
                try:
                    data = finance_data.getFinanceData(cand_name)
                    cand.set_finance_data(data)
                except FileNotFoundError:
                    pass
    
    def get_city_list(self):
        return [{
            'name': city,
            'head_code': sorted(list(regions.keys()))[0]
        } for city, regions in self.city_db.items()]

    def get_region_list(self):
        return [{'id': k, 'name': str(v)} for k,v in self.region_db.items() if v.has_candidate()]

    def get_region(self, id):
        if id in self.region_db:
            return self.region_db[id]
        else:
            return None

    def get_candidate(self, id):
        if id in self.cand_db:
            return self.cand_db[id]
        else:
            return None

if __name__ == '__main__':
    election = Election()
    election.load_data()

    print(election.get_region_list())