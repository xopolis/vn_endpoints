#
# this file is intended to build functions for common tasks 
#

import pandas as pd
from dateutil import parser

def find_profile_experience(dates_list):
    """
    takens in list of datetime strings  
    input : list of durations each separeted by 'to'. 
            Ex: Mar 2018 to Nov 2018, March 2019 to 07/12/2019
    output : Find experience by removing overlaps and return the overall Non-Overlapped Experience in Years
    Reference : https://bit.ly/2UebPGz
    """
    workdates = pd.DataFrame(dates_list,columns=['term'])
    try:
        # series of work START Datetimes
        start = workdates['term'].apply(lambda x:x.split(' to ')[0]).apply(parser.parse)

        # series of work END datetimes
        end = workdates['term'].apply(lambda x:x.split(' to ')[1]).apply(parser.parse)
        #start df
        start_df = pd.DataFrame()
        start_df['timestamp'] = start
        start_df['status'] = 1

        #end_df
        end_df = pd.DataFrame()
        end_df['timestamp'] = end
        end_df['status'] = -1

        df = pd.concat([start_df,end_df]).sort_values('timestamp')

        df['count'] = df['status'].cumsum()
        df['empty'] = (df['count'] == 0).shift().fillna(0).astype(int)
        df['busy'] = df['empty'].cumsum()

        z = df.groupby('busy')['timestamp'].agg([min,max])
        timedeltas = z['max']-z['min']
        experience_days = timedeltas.sum()#datetime object
        experience_years = round(experience_days.days/365,1)
        return experience_years
    except Exception as e:
        print("Err: ",e)
        
        
##--------------------------------------------------------------------------------
#         utility to count and print, for every n iterations
##--------------------------------------------------------------------------------

class count_rate():
    """
    utility to track time and count of #iterations
    prints time(from start) and count in intervals of n(=1000 default) 
    """
    import time
    def __init__(self,n=1000):
        self.n = n
        self.counter = 0
    def count(self): #start counting
        if self.counter == 0:
            self.start_time = self.time.time()
        self.counter += 1
        if self.counter%self.n==0:
            print(f"n-th counter: {self.counter//self.n}   time(s): {round(self.time.time()-self.start_time,2)}")   
    def reset(self):#reset counter
        self.start_time = self.time.time()
        self.counter = 0
        
##--------------------------------------------------------------------------------
#         Merge lists of list of tokens to a single list of tokens 
##--------------------------------------------------------------------------------
import itertools
def merge_lists(LoL):
    """merge list of list of items to a single list 
    [[1,2,3],[4,5,6]] -> [1,2,3,4,5,6]"""
    return list(itertools.chain.from_iterable(LoL))
        
    
##--------------------------------------------------------------------------------
#         Bigrams of a list
##--------------------------------------------------------------------------------
# function to get all bigrams from a list of words
def get_bigram(x):
    BGs = list(zip(x[:-1],x[1:]))
    return list(map(lambda x: tuple(sorted(x)), BGs))

