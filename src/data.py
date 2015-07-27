# data acquirer

import datetime
import os.path
import urllib.request

url_base = 'http://www.nbs.sk/priradenydokument.axd'
data_dir = 'data'
start_date = datetime.date(2007, 1, 1)

def download(url, file_name):
  with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    data = response.read()
    data = data.decode('windows-1250').encode('utf-8')
    out_file.write(data)

def get_months():
  today = datetime.date.today()
  i = start_date
  months = [i.strftime('%y%m')]
  while i.month != today.month or i.year != today.year:
    y = i.year
    m = i.month + 1
    if m > 12:
      y += 1
      m -= 12
    i = datetime.date(y, m, 1)
    months.append(i.strftime('%y%m'))
  return months

def create_url(month):
  return url_base + '?id=ahds' + month + '&type=CSV'

def create_file_name(month):
  return os.path.join(data_dir, 'pfp-' + month + '.csv')

print('Fetching pension fund performance data')
months = get_months()
for month in months:
  url = create_url(month)
  file_name = create_file_name(month)
  print('Downloading ' + url)
  download(url, file_name)
print('Done')

