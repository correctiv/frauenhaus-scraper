import requests
from bs4 import BeautifulSoup
import ast
import os
from datetime import datetime
import json

def formatNewEntry(entry):

	props = entry['properties']
	props['geography'] = entry['geometry']
	props.pop('uid')
	props.pop('freePlacesType')
	props['data'] = []
	return props

fpath = 'frauenhaus_suche.json'

with open(fpath) as f:
	data = json.loads(f.read())

r = requests.get('https://www.frauenhaus-suche.de/')
soup = BeautifulSoup(r.content, 'lxml')
script = soup.find('div', class_='tx-ks-zif-frauenhaus').find_all('script')[1].string.replace('\n','').replace('\t','').replace(';','').split('addressesJson =  ')[1]
d = ast.literal_eval(script)['features']

existing = data.keys()
timestamp = datetime.now().strftime("%d.%m.%Y, %H:%M")

for entry in d:

	uid = entry['properties']['uid']
	freePlaces = entry['properties']['freePlacesType']

	if uid not in existing:

		props = formatNewEntry(entry)
		data[uid] = props

	data[uid]['data'].append({ 'timestamp': timestamp, 'freePlaces': freePlaces })

with open(fpath, 'w') as f:
	json.dump(data, f, indent=4)
