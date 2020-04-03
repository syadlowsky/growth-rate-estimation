# Estimating the growth rate of COVID-19

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Using our analysis code
The main codebase to run our analysis is in `analyze.py`. The `ExponentialGrowthRateEstimator` takes in hyperparameters
`cumulative` (Boolean) indicating whether the counts that will be passed in are cumulative counts or new cases.
`approximate_beta` is used to interpolate missing data (days where the cumulative count is unknown). 
`family` is the generalized linear model family to use: either `Poisson` or `NegativeBinomial`. We recommend
using `NegativeBinomial`, as the variance estimates from the Poisson seem to be a little optimistic, given how
messy COVID-19 count data is. We recommend a default `alpha` value (for the Negative Binomial distribution) of `0.10`
or `0.15`.

Then, pass the numpy vectors `day` indicating the day of a measurement and `cases` indicating the respective
count of new or cumulative cases, to `fit`.

The `growth_rate` and `growth_rate_confint` methods return the growth rate and 95% confidence intervals,
respectively.

## Example usage
A simple example of calling the analysis code is available in `Simple Example.ipynb`. 
See the Jupyter notebooks in `Process States.ipynb` or `Main figures.ipynb` for more complex
examples of how we used this analysis to analyze and plot results for many regions at once.

## Data sourcing
jhu_process_data.py will read the JHU data into: dict['country']['city']=array.
The JHU repository is currently being reformatted so there may be some inconsistencies.

To pull the CSV files for global death data and state-level data, run the following two scripts:

sh pull_global.sh
sh pull_states.sh

You'l probably want to run these roughly daily to keep the sources up to date.
