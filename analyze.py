# Copyright 2019 Steve Yadlowsky

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import statsmodels.api as sm

class ExponentialGrowthRateEstimator(object):
    def __init__(self, cumulative=True):
        self.cumulative = cumulative
        self.glm = None
        self.fitted_glm = None

    def fit(self, day, cases, baseline=None):
        if baseline is None:
            baseline = np.zeros(cases.shape[0])

        covid_cases = cases - baseline
        if self.cumulative:
            covid_cases = np.diff(covid_cases)
            day = day[1:]

        # note: consider using exposure input to subtract baseline cases, as this might automatically handle variance.
        self.glm = sm.GLM(covid_cases, day, family=sm.families.Poisson())
        self.fitted_glm = self.glm.fit()

        return self.fit

    def summary(self):
        if self.fitted_glm is None:
            return "No model fit yet"
        return self.fitted_glm.summary()


def test(active_cases=False):
    days = np.linspace(100, 130)
    new_cases = np.random.poisson(np.exp(0.2 * days))
    total_cases = np.cumsum(new_cases)
    if active_cases:
        total_cases[12:] -= total_cases[:-12]

    model = ExponentialGrowthRateEstimator()
    model.fit(days, total_cases)

    print(model.summary())

if __name__=="__main__":
    test()
    print("Notice that this method is pretty robust to only using active cases:")
    test(active_cases=True)
