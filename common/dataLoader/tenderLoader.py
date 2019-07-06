from datetime import datetime
import requests
import json
import time


def getLatestUpdateTime():
    resp = requests.get('https://pcc.g0v.ronny.tw/api/getinfo')
    if resp.ok:
        return datetime.fromisoformat(json.loads(resp.text)['最新資料時間'])
    else:
        return None


def getWinningBidder(companies_name_key):
    result = []
    for company_name, info in companies_name_key.items():
        is_getting = True
        for val in info:
            if val.find('未得標') >= 0:
                is_getting = False

        if is_getting:
            result.append(company_name)
    return result


def parseTendersPage(json_data, context):
    if 'total_pages' in json_data:
        total_page = json_data['total_pages']
        current_page = json_data['page']
        next_page = current_page + 1 if total_page > current_page else None
    else:
        next_page = None
    
    if 'records' not in json_data:
        return next_page

    for record in json_data['records']:
        brief = record['brief']
        if brief['type'] != '決標公告':
            continue

        context.append({
            'date': record['date'],
            'file_name': record['filename'],
            'unit_name': record['unit_name'],
            'title': brief['title'],
            'amount': 0,
            'winner': getWinningBidder(brief['companies']['name_key'])
        })

    return next_page


def fetchTendersByCompanyName(name):
    next_page = 1
    context = []
    while next_page != None:
        fetch_url = 'https://pcc.g0v.ronny.tw/api/searchbycompanyname?query={}&page={}'.format(
            name, next_page)
        resp = requests.get(fetch_url)
        if resp.ok:
            json_body = json.loads(resp.text)
            next_page = parseTendersPage(json_body, context)
        else:
            return None

    delete_target = []
    for idx in range(len(context)):
        if name not in context[idx]['winner']:
            delete_target.append(context[idx])

    for target in delete_target:
        context.remove(target)

    return context


def fetchTendersByDate(date):
    context = []
    date_str = date.strftime("%Y%m%d")
    fetch_url = 'https://pcc.g0v.ronny.tw/api/listbydate?date={}'.format(
        date_str)
    resp = requests.get(fetch_url)
    if resp.ok:
        json_body = json.loads(resp.text)
        parseTendersPage(json_body, context)
    else:
        return None
    return context


def exportTenderRepository(filename, repository):
    with open(filename, 'w+') as file:
        json.dump(repository, file)


def loadTenderRepository(filename):
    repository = {}
    try:
        with open(filename, 'r') as file:
            repository = json.load(file)
    finally:
        return repository


if __name__ == '__main__':
    context = fetchTendersByDate(datetime(2016, 5, 10))
    print(len(context))
