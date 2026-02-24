###############################
import json
import csv
import datetime as dt
import matplotlib.pyplot as plt
###############################

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva_data.json','r',encoding='ascii')
output_file = open('./eva_data.csv','w',encoding='utf8')
graph_file = './cumulative_eva_graph.png'

data=[]

for i in range(375):
    line=input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
#data.pop(0)
## Comment out this bit if you don't want the spreadsheet

writer=csv.writer(output_file)

time = []
date =[]

j=0
for i in data:
    print(data[j])
    # and this bit
    writer.writerow(data[j].values())
    if 'duration' in data[j].keys():
        duration_str=data[j]['duration']
        if duration_str == '':
            pass
        else:
            hours_mins=dt.datetime.strptime(duration_str,'%H:%M')
            hours = dt.timedelta(hours=hours_mins.hour, minutes=hours_mins.minute,
                                   seconds=hours_mins.second).total_seconds()/(60*60)
            print(hours_mins,hours)
            time.append(hours)
            if 'date' in data[j].keys():
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

time_axis=[0]
for i in time:
    time_axis.append(time_axis[-1]+i)

date,time = zip(*sorted(zip(date, time)))

plt.plot(date,time_axis[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
