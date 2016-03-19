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

counts = dict()

frequency_list=[
"Not Applicable",
"5-Years",
"5-years",
"Annual, As of July 1",
"Annual, End of Year",
"Annual, Fiscal Year",
"Annual, End of Period",
"Annual, As of January 1",
"Annual",
"Semiannual",
"Quarterly",
"Quarterly, End of Period",
"Quarterly, Beginning of Period",
"Quarterly, End of Quarter",
"Quarterly, 1st Full Wk. in 2nd Mo. Of Qtr.",
"Monthly",
"Monthly, End of Period",
"Monthly, Middle of Month",
"Monthly, End of Month",
"Monthly, Saturday Nearest Month's End",
"Monthly, END AND MIDDLE OF THE MONTH",
"Monthly, As of 15th of the Month",
"Bi-Weekly, Ending Wednesday",
"Bi-Weekly, Beg. of Period",
"Bi-Weekly, Ending Monday",
'Bi-Weekly, Ending Monday',
'Weekly, As of Monday',
"Weekly, As of Monday",
"Weekly, As of Wednesday",
"Weekly, Ending Thursday",
"Weekly",
"Weekly, Ending Saturday",
"Weekly, Ending Wednesday",
"Weekly, Ending Friday",
"Weekly, Ending Monday",
"Weekly, As of Thursday",
"Daily",
"Daily, Seven Day",
"Daily, Close"
]



conn = sqlite3.connect("dataset.sqlite")
conn.execute("drop table if exists metrics")
conn.execute("create table if not exists metrics (seriesid varchar(200), title varchar(250), units varchar(250), datastart varchar(250), path varchar(255), frequency integer, primary key (seriesid ASC));")
cursor = conn.cursor()
insert_query="insert or replace into metrics (seriesid, title, units, datastart, path, frequency) values(?,?,?,?,?,?)"

def import_header_data(filename):
    data = {}
    with open(filename) as datafile:
        for num, line in enumerate(datafile, 1):
            if ':' in line:
                (key,value) = line.split(':',1)
                data[key] = value.strip()
            if re.match('DATE\s*VALUE', line):
                freq = data['Frequency'].decode("utf8")
                data['DataStart']= num + 1
                series_id=unicode(data['Series ID'].decode("utf8"))
                title=unicode(data['Title'].decode("utf8"))
                units=unicode(data['Units'].decode("utf8"))
                datastart=unicode(data['DataStart'])
                filename=unicode(filename)
                freq_idx=unicode(frequency_list.index(freq))
                return (series_id, title, units, datastart, filename, freq_idx)
    return None

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root,name))
    return result

filelist=find('*.txt', 'FRED2_txt_2')
                  
idx = 0
pp = pprint.PrettyPrinter(indent=4)
dataset = []
for filename in filelist:
    idx = idx + 1
    result = import_header_data(filename)

    if (not result is None):
      word_list = re.findall(r"\w+",result[1])
      for word in word_list:
        counts[word]=counts.get(word,0) + 1
      dataset.append(result) 
    if (idx % 10000 == 0):
        cursor.executemany(insert_query,dataset)
        dataset=[]
        conn.commit()

pp.pprint(counts)
