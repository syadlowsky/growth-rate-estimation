#!/bin/sh
mkdir -p data
wget http://covidtracking.com/api/states/daily.csv
mv daily.csv data/states-daily.csv
