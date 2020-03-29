import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from math import sqrt
import analyze
from itertools import chain

f = open('data/states-daily.csv')
reader = csv.reader(f)
first = True
rows = []

num_cols = 24
def default():
  return np.zeros(shape=(num_cols,))
def intsafe(x):
  return int(x) if x != '' else -1
tests = defaultdict(default)
hosps = defaultdict(default)
deaths = defaultdict(default)
for row in reader:
  if first:
    columns = row
    first = False
  else:
    day = int(row[0]) - 20200301
    state = row[1]
    test_count = intsafe(row[-2])
    death_count = intsafe(row[-3])
    hosp_count = intsafe(row[-4])
    tests[state][day] = test_count
    hosps[state][day] = hosp_count
    deaths[state][day] = death_count

def calculate_growth(series, thresh=10, start=5):
  days = np.arange(0, series.shape[0])
  if ((series < thresh).all()):
    return None
  keep = series >= start
  series = series[keep]
  days = days[keep]
  if (days.shape[0] < 5):
    return None
  print(series)
  print(days)
  model = analyze.ExponentialGrowthRateEstimator(family='NegativeBinomial', alpha=None)
  model.fit(day=days, cases=series)
  print(np.diff(series))
  print(model.fitted_glm.mu)
  est = model.growth_rate()
  low, high = model.growth_rate_confint()
  return (max(low, 0), est, high)

growths = dict()
dataset = deaths.items()
for k, v in dataset:
  #try:
  growth = calculate_growth(v, thresh = 20, start = 4)
  if growth:
    print(' (for %s)' % k)
    growths[k] = growth
  #except Exception:
  #  print('Failed to calculate for %s' % k)

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
