import csv
from collections import defaultdict
import numpy as np
from math import sqrt
import analyze
from itertools import chain

f = open('data.csv')
reader = csv.reader(f)
first = True
rows = []

def default():
  return np.zeros(shape=(59,))
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
    if row[1] == 'US':
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

growths = dict()
for k, v in chain(agg_counts.items(), region_counts.items()):
  growth = calculate_growth(v, thresh = 20, start = 5)
  if growth:
    growths[k] = growth
#us_growth = dict()
#for k, v in us_counts.items():
#  if k == 'King County, WA':
#    continue
#  g = calculate_growth(v)
#  if g and g[0] > 0:
#    us_growth[k] = g

import matplotlib.pyplot as plt
to_plot = growths
names = list(to_plot.keys())
err_l = list([v[1]-v[0] for v in to_plot.values()])
ests  = list([v[1] for v in to_plot.values()])
err_h = list([v[2]-v[1] for v in to_plot.values()])
errs = np.array([err_l, err_h])
plt.bar(range(len(names)), ests, yerr=errs, align='center')

plt.xticks(range(len(names)), names)
plt.show()
