import numpy as np

import analyze

# Deaths (cumulative)
deaths = np.array(
    [1, 2, 3, 5, 10, 17, 28, 35, 54, 55, 133, 195, 289, 342, 533, 623, 830, 1043]
)  # Mar 3 through Mar 20
days = np.array(range(2, 20))  # days since Mar 1

print(deaths, days)

model = analyze.ExponentialGrowthRateEstimator(cumulative=True)
model.fit(day=days, cases=deaths)
print(model.summary())
print("Growth rate is {}".format(model.growth_rate()))
