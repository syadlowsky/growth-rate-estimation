import numpy as np

import analyze

# Hospitalizations
cases = np.array([4, 11, 37, 38, 48, 52, 56, 62, 65, 93, 108])
days = np.array([2, 3, 12, 13, 14, 15, 17, 18, 19, 20, 21])

# Total cases
#cases = np.array([4, 7, 9, 11, 14, 20, 24, 32, 37, 43, 45, 48, 79, 91, 114, 138, 155, 175, 189, 196, 263, 302])
#days = np.arange(0, cases.shape[0])

print(cases, days)

model = analyze.ExponentialGrowthRateEstimator(cumulative=True, approximate_beta=0.2)
model.fit(days, cases)
print(model.summary())
print("Growth rate is {}".format(model.growth_rate()))
