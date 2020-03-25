import pandas as pd
import numpy as np
import datetime 

#given date d, finds nearest future date that falls on given weekday value, where weekday=0 is monday
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


#pass in raw csv of 2017-2020 e.g. csv="NYC_ILI_2017-2020.csv",disease_type="ILI"
#saves raw baseline data and quintiles baseline in pkls
def get_baselines(csv,disease_type,save_dir='data/'):
    df = pd.read_csv(csv,infer_datetime_format=True,encoding='latin')
    df['Date'] = pd.to_datetime(df['Date'],infer_datetime_format=True)
    df['Count'] = pd.to_numeric(df['Count'].str.replace(",",""))
    xs,ys = [],[]
    #get most recent two weeks
    for year in [2017,2018,2019]:
        d = datetime.date(year, 1, 1)
        end_date = pd.Timestamp(datetime.date(year,df['Date'].max().month,df['Date'].max().day))
        #next_monday = pd.Timestamp(next_weekday(d, 0))
        next_monday = end_date - pd.Timedelta(days=14)
        this_slice = df[(df['Date']>=next_monday)&(df['Date']<=end_date)]
        if year== 2020:
            this_slice = this_slice[(this_slice['Dim2Value']=='All age groups')&(this_slice['Dim1Value']=='Citywide')]
        x = this_slice['Date'].dt.weekday.values
        y = this_slice['Count'].values
        xs.append(x)
        ys.append(y)

    xs = np.concatenate(xs).ravel()
    ys = np.concatenate(ys).ravel()

    df = pd.DataFrame(np.array([xs,ys]).T,columns=['Day of Week','Count'])
    #save raw data for all years
    df.to_pickle(save_dir+"raw_baseline_2017-2019_mostrecent2wks_"+disease_type+".pkl")
    quantiles = df.groupby(["Day of Week"]).quantile()
    quantiles['mean'] = quantiles['Count']
    quantiles = quantiles.drop("Count",axis=1)
    quantiles['20%'] = df.groupby(["Day of Week"]).quantile(0.2)
    quantiles['80%'] = df.groupby(["Day of Week"]).quantile(0.8)
    #save just quintiles
    quantiles.to_pickle(save_dir+"baseline_percentiles_2017-2019_mostrecent2wks_"+disease_type+".pkl")