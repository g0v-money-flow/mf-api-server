from .model.election import Election
from .dataSource import election_data

election = election_data.Election()
election.load_data()

def loadData():
    e2020 = Election(2020)
    return {
        'legislator':{
            '2016': election,
            '2020': e2020
        }
    }

data = loadData()