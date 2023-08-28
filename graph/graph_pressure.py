


import requests #used to make api call
import json #json lib
import time
import pandas as pd


BASE_ADDRESS = 'http://192.168.3.213:5000'
path_api = 'Pressure'
sub_area = '/date'
path_variables = '?LoadDate=2023-08-24T00:00:00'
#x = requests.get('https://h4motion.victorkrogh.dk/api/v1/device/sessions/8EC325DE-A87F-43F5-B1B8-69437593895B/humidity')
#x = requests.get(f'{BASE_ADDRESS}/{path_api}')
x = requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
data_json = x.content
# print(data_json)
data = json.loads(data_json)
print(data)
# print(data["Temperature"])
df = pd.DataFrame(data["Pressure"])
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
plt.plot(df.index, df['PressureInHectoPascal'])

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

plt.title('Pressure over Time')
plt.xlabel('LoadDate')
plt.ylabel('Pressure')

plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates

# Convert 'LoadDate' column to LoadDatetime type
#df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set 'LoadDate' as the index
# df.set_index('timestamp', inplace=True)

# # Plot the data
# plt.figure(figsize=(10, 6))
# plt.plot(df.index, df['temperatureCelsius'])

# # Format the x-axis to display LoadDates properly
# plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d'))
# plt.gca().xaxis.set_major_locator(mLoadDates.DayLocator(interval=10))

# plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

# plt.title('Temperature over Time')
# plt.xlabel('timestamp')
# plt.ylabel('temperatureCelsius')

# plt.show()

# def tempfuntion(path_api):
#     global BASE_ADDRESS
#     # data = get_data_func()

#     # json_str = format_json_func(data)
    
#     # json_object = json.loads(json_str)

#     print(x.status_code)
#     #requests.post(BASE_ADDRESS + "/" + path_api,json = json_object)
#     if x.status_code == 200:
#         print (x.json())
#     #print(x.body)

# while True:
#     #Miljø
#     tempfuntion('Temperature')
#     tempfuntion('Pressure')
#     tempfuntion('Humidity')
#     time.sleep(5)
#     #IMU DegreesToNorth
#     # tempfuntion('Accelerometer',sense.get_accelerometer, lambda data : '{"Pitch" :' + str(data["pitch"]) + ', "Roll" :' + str(data["roll"]) + ', "Yaw" :' + str(data["yaw"]) + '}')
#     # tempfuntion('Compass',sense.get_compass, lambda data : '{"DegreesToNorth" :' + str(data) + '}')
#     #tempfuntion('Accelerometer',sense.get_accelerometer, lambda data : '{"Pitch" :' + str(data["pitch"]) + ', "Roll" :' + str(data["roll"]) + ', "Yaw" :' + str(data["yaw"]) + '}')
#     #tempfuntion('Accelerometer',sense.get_accelerometer, lambda data : '{"Pitch" :' + str(data["pitch"]) + ', "Roll" :' + str(data["roll"]) + ', "Yaw" :' + str(data["yaw"]) + '}')
