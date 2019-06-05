from .model.election import Election

def loadData():
    e2016 = Election(2016)
    e2020 = Election(2020)
    return {
        'legislator':{
            '2016': e2016,
            '2020': e2020    
        }
    }

data = loadData()