#!/bin/sh
wget http://covidtracking.com/api/states/daily.csv
mv daily.csv data/states-daily.csv
