import os
import sys
import time

class FundCategory:
  def __init__(self, name, number):
    self.name = name
    self.number = number
    self.funds = {}

class Fund:
  def __init__(self, name, number):
    self.name = name
    self.number = number
    self.data = []

  def update(self, values):
    self.data.extend(values)

class DataPoint:
  def __init__(self, date, value):
    self.date = date
    self.value = value

fund_categories = {}
data_dir = 'data'

def process_line(line):
  line = line.strip()
  values = line.split(';')
  if values[1] == '':
    return True, values[0]
  return False, values

def process_values(dates, values):
  data = []
  for d, v in zip(dates, values):
    dt = time.strptime(d, '%d.%m.%Y')
    data.append(DataPoint(dt, v))
  return data

def load_file(file_name):
  with open(file_name, 'r') as pfp_file:
    pfp_file.readline()
    
    date_line = pfp_file.readline()
    date_line = date_line.strip()
    dates = date_line.split(';')[1:]

    fund_category = 'unknown'
    while True:
      line = pfp_file.readline()
      if not line: break
      
      is_header, data = process_line(line)
      if is_header:
        fund_category = data
        if fund_category not in fund_categories:
          fund_categories[fund_category] = \
            FundCategory(fund_category, len(fund_categories) + 1)
      else:
        fund_name = data[0]
        values = data[1:]
        fund_group = fund_categories[fund_category]
        if fund_name not in fund_group.funds:
          fund_group.funds[fund_name] = \
            Fund(fund_name, len(fund_group.funds) + 1)
        fund = fund_group.funds[fund_name]
        values = process_values(dates, values)
        fund.update(values)

def list_data():
  for fund_category in fund_categories:
    fund_category = fund_categories[fund_category]
    print(str(fund_category.number) + ': ' + fund_category.name)
    for fund in fund_category.funds:
      fund = fund_category.funds[fund]
      print('* ' + str(fund.number) + ': ' + fund.name
        + ' (' + str(len(fund.data)) + ' records, first '
        + time.strftime("%d/%m/%Y", fund.data[0].date) + ', last '
        + time.strftime("%d/%m/%Y", fund.data[-1].date)  + ')')
    print()

def show_detail(fund_category, fund):
  print(fund_category.name + ' - ' + fund.name)
  for day in fund.data:
    print(time.strftime('%Y-%m-%d', day.date), end='')
    print(': ', end='')
    print(day.value, end='')
    print()
  print()

def detail():
  print('Choose a fund category')
  line = sys.stdin.readline().strip()
  fund_category_id = int(line)
  for name, fund_category in fund_categories.items():
    if fund_category.number == fund_category_id:
      fund_category = fund_category
      break
  
  print('Choose a fund')
  line = sys.stdin.readline().strip()
  fund_id = int(line)
  for name, fund in fund_category.funds.items():
    if fund.number == fund_id:
      break

  show_detail(fund_category, fund)

def load_data():
  fund_categories.clear()
  
  print('Enter how many months to load')
  line = sys.stdin.readline().strip()
  months = int(line)
  
  pfp_files = os.listdir(data_dir)
  pfp_files = pfp_files[-months:]
  load_files(pfp_files)

def load_all_data():
  fund_categories.clear()
  pfp_files = os.listdir(data_dir)
  load_files(pfp_files)

def load_files(pfp_files):
  for pfp_file in pfp_files:
    load_file(os.path.join(data_dir, pfp_file))
  list_data()

def menu():
  print('Choose option:\n'
        ' d: detail\n'
        ' l: load data\n'
        ' q: quit')

load_all_data()
menu()
for cmd in sys.stdin:
  cmd = cmd.strip()
  if cmd == 'd':
    detail()
  elif cmd == 'l':
    load_data()
  elif cmd == 'q':
    break
  menu()

print('Goodbye!')

