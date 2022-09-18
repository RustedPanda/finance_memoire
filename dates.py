# -*- coding: utf-8 -*-
"""
Created on Sun May 22 16:55:42 2022

@author: ludo_
"""

"""
We can't use the easy date generation method of pd.date_range() for example
as the date format needed for the API is quite different 
(e.g. 2021-01-01T00:00:00.000Z)
Note the T and Z smugling in the date

We therefore need to manually create a list of dates for a given year
"""

def date_format(year,month,day,hour):
    
    dates = []
    
    if month < 10 and day < 10 and hour < 10:
        dates.append(str(year)+'-0'+str(month)+'-0'+str(day)+'T0'+str(hour)+':00:00.000Z')
    elif month < 10 and day >= 10 and hour < 10:
        dates.append(str(year)+'-0'+str(month)+'-'+str(day)+'T0'+str(hour)+':00:00.000Z')
    elif month >= 10 and day < 10 and hour < 10:
        dates.append(str(year)+'-'+str(month)+'-0'+str(day)+'T0'+str(hour)+':00:00.000Z')
    elif month>= 10 and day >= 10 and hour < 10:
        dates.append(str(year)+'-'+str(month)+'-'+str(day)+'T0'+str(hour)+':00:00.000Z')
    elif month>= 10 and day < 10 and hour >= 10:
        dates.append(str(year)+'-'+str(month)+'-0'+str(day)+'T'+str(hour)+':00:00.000Z')
    elif month>= 10 and day >= 10 and hour >= 10:
        dates.append(str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+':00:00.000Z')
    elif month< 10 and day < 10 and hour >= 10:
        dates.append(str(year)+'-0'+str(month)+'-0'+str(day)+'T'+str(hour)+':00:00.000Z')
    elif month< 10 and day >= 10 and hour >= 10:
        dates.append(str(year)+'-0'+str(month)+'-'+str(day)+'T'+str(hour)+':00:00.000Z')
        
    return dates

def generate_dates_start(year):

    dates = []
    
    if(year%4==0 and year%100!=0 or year%400==0):
        bis = True
    else :
        bis = False
    
    for month in range(1,13):
        if month in [1,3,5,7,8,10,12] :
            for day in range(1,32):
                for hour in range(0,24):
                    dates.append(date_format(year, month, day, hour))
        elif month in [4,6,9,11] :
            for day in range(1,31):
                for hour in range(0,24):
                    dates.append(date_format(year, month, day, hour))
        elif month == 2 :
            if bis == True :
                for day in range(1,30):
                    for hour in range(0,24):
                        dates.append(date_format(year, month, day, hour))
            else : 
                for day in range(1,29):
                    for hour in range(0,24):
                        dates.append(date_format(year, month, day, hour))
    return dates

def generate_dates_end(dates,year):
    
    end_list = dates[1:] + dates[:1]
    
    return end_list