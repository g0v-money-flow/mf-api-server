#!/usr/bin/python
# coding:utf-8

import csv
import sys
import os

# support multiple csv file (收入明細.csv and 支出明細.csv))))
filenames = sys.argv[1:]


def exportResult(folder, filename, result):
  if not os.path.exists(folder):
    os.makedirs(folder)

  with open('{}/{}'.format(folder, filename), 'w') as file:
    writer = csv.writer(file)
    writer.writerow([
      '序號',
      '交易日期',
      '收支科目',
      '捐贈者/支出對象',
      '身分證/統一編號',
      '收入金額',
      '支出金額',
      '金錢類',
      '地址'
    ])

    for row in result:
      income = int(float(row['income']))
      outcome = int(float(row['outcome']))
      if income == 0:
        income = None
      if outcome == 0:
        outcome = None

      writer.writerow([
        1,
        row['date'],
        row['record_type'],
        row['record_obj'],
        row['id_number'],
        income,
        outcome,
        'a',
        row['address']
      ])


result = {}

for name in filenames:
  with open(name, 'r') as file:
    reader = csv.reader(file)

    isFirstLine = True
    for line in reader:
      if isFirstLine:
        isFirstLine = False
        continue

      date = line[5]
      date = '{}/{}/{}'.format(date[0:-4], date[-4:-2], date[-2:])

      region = line[0]
      name = line[2]
      election = line[3]
      record_type = line[6]
      record_obj = line[7]
      id_number = line[8]
      income = line[9]
      outcome = line[10]
      address = line[13]

      key = '{}-{}-{}'.format(election, region, name)
      if key not in result:
        result[key] = []
      recordList = result[key]
      recordList.append({
        'election': election,
        'date': date,
        'record_type': record_type,
        'record_obj': record_obj,
        'id_number': id_number,
        'income': income,
        'outcome': outcome,
        'address': address
      })

if not os.path.exists('output'):
    os.makedirs('output')

for k, v in result.items():
  key_part = k.split('-')
  electionName = key_part[0]
  candidate = '{}-{}.csv'.format(key_part[1], key_part[2])
  folderName = 'output/{}/'.format(electionName)
  exportResult(folderName, candidate, v)
