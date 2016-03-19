#Title:               Motor Vehicle Assemblies: Truck assemblies
#Series ID:           MVATRUCKSN
#Source:              Board of Governors of the Federal Reserve System (US)
#Release:             G.17 Industrial Production and Capacity Utilization
#Seasonal Adjustment: Not Seasonally Adjusted
#Frequency:           Monthly
#Units:               Millions of Units
#Date Range:          1965-01-01 to 2015-04-01
#Last Updated:        2015-05-15 9:07 AM CDT
#Notes:               Source Code: MVA.TRUCKS.N

import pprint
import re
import os, fnmatch
import sqlite3
import pandas as pd
from dateutil.parser import parse
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
pp = pprint.PrettyPrinter(indent=4)

conn = sqlite3.connect("dataset.sqlite")
cursor = conn.execute("select title, datastart,path from metrics limit 1;")
(title, datastart, path) = cursor.fetchone()

data=pd.read_csv('/home/tj/dev/python-econ/FRED2_txt_2/data/0/00XAPFESM086NEST.txt',sep='\s+',parse_dates=['DATE'],date_parser=dateparse, header=43, engine='python')
result = data.set_index('DATE').resample('A', how='mean')
print(title, datastart, path)
pp.pprint(result.iloc[0]['VALUE'])





#def import_header_data(filename):
#    data = {}
#    conn = sqlite3.connect("dataset.sqlite", isolation_level=None)
#    cursor = conn.cursor()
#    with open(filename) as datafile:
#        for num, line in enumerate(datafile, 1):
#            if ':' in line:
#                (key,value) = line.split(':',1)
#                data[key] = value.strip()
#            if re.match('DATE\s*VALUE', line):
#                data['DataStart']= num + 1
#                pp = pprint.PrettyPrinter(indent=4)
#                try:
#                  pp.pprint(data['Title'])
#                  cursor.execute("insert or replace into metrics (title, units, datastart, path) values(?,?,?,?)", (data['Title'],data['Units'],data['DataStart'],filename))
#                  conn.commit
#                except sqlite3.Error, e:
#                    print "Error: %s" % e.args[0]
#    return data
#
#def find(pattern, path):
#    result = []
#    for root, dirs, files in os.walk(path):
#        for name in files:
#            if fnmatch.fnmatch(name, pattern):
#                result.append(os.path.join(root,name))
#    return result
#
#filelist=find('*.txt', '.')
#                  
#pp = pprint.PrettyPrinter(indent=4)
#for filename in filelist:
#    result = import_header_data(filename)
#    print("---------------------------------------" + filename)
#    pp.pprint(result)
