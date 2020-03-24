import csv
from collections import defaultdict
import numpy as np
from math import sqrt
import analyze
from itertools import chain

f = open('data/time_series_covid19_deaths_global.csv')
reader = csv.reader(f)
first = True
rows = []

num_cols = 62
def default():
  return np.zeros(shape=(num_cols,))
province_counts = defaultdict(default)
agg_counts = defaultdict(default)
region_counts = defaultdict(default)
us_counts = defaultdict(default)
for row in reader:
  if first:
    columns = row
    first = False
  else:
    rows.append(row)
    series = np.array(list(map(float, row[4:])))
    if row[0] == '':
      region_counts[row[1]] = series
    else:
      province_counts[row[0]] = series
      agg_counts[row[1]] += series
# for US data
f = open('data/time_series_19-covid-Deaths.csv')
reader = csv.reader(f)
first = True
for row in reader:
  if first:
    first = False
  else:
    print(row)
    if row[1] == 'US' and row[0] != 'US' and row[0][-4] != ',':
      series = np.array(list(map(float, row[4:-1])))
      us_counts[row[0]] = series

def calculate_growth(series, thresh=10, start=5):
  days = np.arange(0, series.shape[0])
  if ((series < thresh).all()):
    return None
  keep = series >= start
  series = series[keep]
  days = days[keep]
  model = analyze.ExponentialGrowthRateEstimator()
  model.fit(day=days, cases=series)
  est = model.growth_rate()
  low, high = model.growth_rate_confint()
  return (max(low, 0), est, high)

for k, v in region_counts.items():
  if k in agg_counts.keys():
    if np.any(agg_counts[k] != v):
      print('WARNING: Counts do not match for %s: %d vs %d' % (k, v[-1], agg_counts[k][-1]))
      del agg_counts[k]
    else:
      print('Passed check for %s' % k)

growths = dict()
skip = ['Austria', 'Denmark', 'China']
#dataset = chain(agg_counts.items(), region_counts.items()):
dataset = us_counts.items()
for k, v in dataset:
  if k in skip:
    continue
  try:
    growth = calculate_growth(v, thresh = 20, start = 5)
    if growth:
      growths[k] = growth
  except Exception:
    print('Failed to calculate for %s' % k)

import matplotlib.pyplot as plt
to_plot = growths
names = list(to_plot.keys())
err_l = list([v[1]-v[0] for v in to_plot.values()])
ests  = list([v[1] for v in to_plot.values()])
err_h = list([v[2]-v[1] for v in to_plot.values()])
errs = np.array([err_l, err_h])
plt.rcParams['axes.axisbelow'] = True
plt.bar(range(len(names)), ests, yerr=errs, align='center')
plt.ylim([0,0.8])
plt.grid(axis='y')

plt.xticks(range(len(names)), names)
plt.show()
