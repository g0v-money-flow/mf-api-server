import os
import re

FOLDER_NAME_PATTERN = re.compile('^[a-z]+[0-9]+$')


def findDataSource(folderName):
    if not re.match(FOLDER_NAME_PATTERN, folderName):
        return None

    root = 'common/dataSource/rawData/{}'.format(folderName)
    name = re.findall('^[a-z]+', folderName)[0]
    year = re.findall('[0-9]+$', folderName)[0]

    res = {
        'name': name,
        'year': year
    }
    for f in os.listdir(root):
        if re.match('^elcand.+csv$', f):
            res['cand_file'] = '{}/{}'.format(root, f)
        elif re.match('^elctks.+csv$', f):
            res['tks_file'] = '{}/{}'.format(root, f)
        elif re.match('^elbase.+csv$', f):
            res['base_file'] = '{}/{}'.format(root, f)
        elif re.match('^elpa.?ty.*csv$', f):
            res['party_file'] = '{}/{}'.format(root, f)
    return res


def findAllData():
    folders = os.listdir('common/dataSource/rawData/')
    return [findDataSource(f) for f in folders]
