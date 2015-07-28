import os
import sys
import time

class FundCategory:
  def __init__(self, name):
    self.name = name
    self.funds = {}

class Fund:
  def __init__(self, name):
    self.name = name
    self.data = []

  def update(self, values):
    self.data.extend(values)

class DataPoint:
  def __init__(self, date, value):
    self.date = date
    self.value = value

fund_categories = {}
data_dir = 'data'

def read_line(line):
  values = line.split(';')
  if values[1] == '':
    return True, values[0]
  return False, values

def process_values(dates, values):
  data = []
  for d, v in zip(dates, values):
    dt = time.strptime(d.strip(), '%d.%m.%Y')
    data.append(DataPoint(dt, v))
  return data

def load_file(file_name):
  with open(file_name, 'r') as pfp_file:
    pfp_file.readline()
    
    date_line = pfp_file.readline()
    dates = date_line.split(';')[1:]

    fund_category = 'unknown'
    while True:
      line = pfp_file.readline()
      if not line: break
      
      is_header, data = read_line(line)
      if is_header:
        fund_category = data
        if fund_category not in fund_categories:
          fund_categories[fund_category] = FundCategory(fund_category)
      else:
        fund_name = data[0]
        values = data[1:]
        fund_group = fund_categories[fund_category]
        if fund_name not in fund_group.funds:
          fund_group.funds[fund_name] = Fund(fund_name)
        fund = fund_group.funds[fund_name]
        values = process_values(dates, values)
        fund.update(values)

def list_data():
  for fund_category in fund_categories:
    print(fund_category)
    for fund in fund_categories[fund_category].funds:
      fund = fund_categories[fund_category].funds[fund]
      print('* ' + fund.name + ' (' + str(len(fund.data)) + ' records)')
    print()

pfp_files = os.listdir(data_dir)
for pfp_file in pfp_files:
  load_file(os.path.join(data_dir, pfp_file))
list_data()

print('Done')

