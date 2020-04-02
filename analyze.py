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
    def __init__(self, cumulative=True, approximate_beta=0.2, family="NegativeBinomial", alpha=0.1):
        self.cumulative = cumulative
        self.glm = None
        self.fitted_glm = None
        self.approximate_beta = approximate_beta
        self.family = family
        self.alpha = alpha

    def fit(self, day, cases, baseline=None):
        if baseline is None:
            baseline = np.zeros(cases.shape[0])

        covid_cases = cases - baseline
        if self.cumulative:
            # Not totally convinced this is the right way to handle irregular intervals. It seems to work ok, though. It is robust, but I don't know how biased it is.
            covid_cases = np.diff(covid_cases).astype(float)
            exposure_lengths = np.diff(day).astype(float)
            covid_cases /= exposure_lengths
            exposure_adjustment = self._exposure_adjustment(exposure_lengths)
            print(exposure_adjustment)
            day = day[1:] + exposure_adjustment

        if self.family == "Poisson":
            fam = sm.families.Poisson()
        if self.family == "NegativeBinomial":
            alpha = self.alpha
            if alpha is None:
                print("Please specify a value of alpha to use with the NegativeBinomial distribution")
            fam = sm.families.NegativeBinomial(alpha=alpha)

        self.glm = sm.GLM(covid_cases, sm.add_constant(day), family=fam)
        self.fitted_glm = self.glm.fit()

        return self.fitted_glm

    def _exposure_adjustment(self, delta_ts):
        return np.array([self._exposure_adjustment_for_interval_length(delta_t) for delta_t in delta_ts])

    def _exposure_adjustment_for_interval_length(self, delta_t):
        return np.log(np.sum(np.exp(self.approximate_beta * np.arange(delta_t))) / delta_t) / self.approximate_beta

    def summary(self):
        if self.fitted_glm is None:
            return "No model fit yet"
        return self.fitted_glm.summary()

    def growth_rate(self):
        if self.fitted_glm is None:
            return "No model fit yet"
        return np.exp(self.fitted_glm.params[1]) - 1

    def growth_rate_confint(self):
        if self.fitted_glm is None:
            return "No model fit yet"
        confint = self.fitted_glm.conf_int(cols=(1,))
        return np.exp(confint[0, 0]) - 1, np.exp(confint[0, 1]) - 1

def test(active_cases=False):
    days = np.arange(100, 130)
    new_cases = np.random.poisson(np.exp(0.2 * days))
    total_cases = np.cumsum(new_cases)
    if active_cases:
        total_cases[12:] -= total_cases[:-12]

    model = ExponentialGrowthRateEstimator()
    model.fit(days, total_cases)

    print(model.summary())

def test_exposure_adjustment():
    test_object = ExponentialGrowthRateEstimator(approximate_beta=0.2)
    print(test_object._exposure_adjustment_for_interval_length(1))
    print(test_object._exposure_adjustment_for_interval_length(2))
    print(test_object._exposure_adjustment_for_interval_length(3))

if __name__=="__main__":
    test_exposure_adjustment()
    test()
    print("Notice that this method is pretty robust to only using active cases:")
    test(active_cases=True)
