import csv
from collections import defaultdict
import numpy as np
from math import sqrt
import analyze
from itertools import chain

f = open('data/ILINet.csv')
reader = csv.reader(f)
first = True
rows = []
count = 0

key_map = {
  'AGE 0-4' : '0-4', 
  'AGE 5-24' : '5-24', 
  'AGE 25-49' : '25-49', 
  'AGE 25-64' : '25-64', 
  'AGE 50-64' : '50-64', 
  'AGE 65' : '65+', 
  'ILITOTAL' : 'All',
}

states = defaultdict(dict)

for row in reader:
  if count < 2:
    columns = row
  else:
    rows.append(row)
    row_dict = dict(zip(columns, row))
    if row_dict['REGION TYPE'] == 'States' and row_dict['YEAR'] == '2020':
      state = row_dict['REGION']
      state_dict = dict()
      for k1, k2 in key_map.items():
        if row_dict[k1] != 'X':
          state_dict[k2] = row_dict[k1]
      states[state][int(row_dict['WEEK'])] = state_dict
  count += 1

weeks = 11
def default():
  return np.zeros(shape=(11,))
states_np = defaultdict(default)
for k in states.keys():
  for ii in range(weeks):
    try:
      states_np[k][ii] = int(states[k][ii+1]['All'])
    except KeyError:
      states_np[k][ii] = -1
