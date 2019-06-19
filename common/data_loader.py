from .model.election import Election
from .dataSource import election_data

def load_data():
    e2020 = Election(2020)
    return {
        'legislator':{
            '2016': election,
            '2020': e2020
        }
    }

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
    
election = election_data.Election()
election.load_data()
data = load_data()