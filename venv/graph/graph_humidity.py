
import requests #used to make api call
import json #json lib
import time
import pandas as pd


BASE_ADDRESS = 'http://192.168.3.213:5000'
path_api = 'Humidity'
sub_area = '/date'
path_variables = '?LoadDate=2023-08-24T00:00:00'
#x = requests.get('https://h4motion.victorkrogh.dk/api/v1/device/sessions/8EC325DE-A87F-43F5-B1B8-69437593895B/humidity')
#x = requests.get(f'{BASE_ADDRESS}/{path_api}')
x = requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
data_json = x.content
# print(data_json)
data = json.loads(data_json)
# print(data["Temperature"])
df = pd.DataFrame(data["Humidity"])
del df["ID"]
# del df["deviceSessionId"]
# del df["humidityPercentage"]
# del df["created"]
# del df["modified"]
print(df)

import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates

# Convert 'LoadDate' column to LoadDatetime type
df['LoadDate'] = pd.to_datetime(df['LoadDate'])
print(df['LoadDate'])
# Set 'LoadDate' as the index
df.set_index('LoadDate', inplace=True)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Humidity'])

# Format the x-axis to display LoadDates properly
# plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d %H:%M:%S'))
#plt.gca().xaxis.set_major_formattermyFmt = mLoadDates("%Y-%m-%d %H:%M:%S")
# plt.gca().xaxis.set_major_formatter(myFmt))
# myFmt = mLoadDates("%Y-%m-%d %H:%M:%S")
# plt.gca().xaxis.set_major_formatter(myFmt)
# plt.gca().xaxis.set_major_locator(mLoadDates.DayLocator(interval=500))
plt.gca().xaxis.set_major_locator(mLoadDates.MinuteLocator(interval=250))

plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

plt.title('Humidity over Time')
plt.xlabel('LoadDate')
plt.ylabel('Humidity')

plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates


