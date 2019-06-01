from .model.election import Election

def loadData():
    return [Election(2016), Election(2020)]

data = loadData()