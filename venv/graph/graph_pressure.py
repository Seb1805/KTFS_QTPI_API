import requests #used to make api call
import json #json lib
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates


BASE_ADDRESS = 'http://192.168.3.213:5000'
path_api = 'Pressure'
sub_area = '/date'
path_variables = '?LoadDate=2023-08-24T00:00:00'
x = requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
data_json = x.content
data = json.loads(data_json)
print(data)
df = pd.DataFrame(data["Pressure"])
del df["ID"]

# Convert 'LoadDate' column to LoadDatetime type
df['LoadDate'] = pd.to_datetime(df['LoadDate'])
# Set 'LoadDate' as the index
df.set_index('LoadDate', inplace=True)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['PressureInHectoPascal'])

# Format the x-axis to display LoadDates properly
plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mLoadDates.MinuteLocator(interval=250))

plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

plt.title('Pressure over Time')
plt.xlabel('LoadDate')
plt.ylabel('Pressure')

plt.show()
