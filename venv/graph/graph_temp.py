
#import requests #used to make api call
import requests_async as requests
import json #json lib
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates
import matplotlib.style as mplstyle
import sys
import threading
import asyncio


mplstyle.use('fast')
async def main():
    img = await plot_to_img()
    return img

# sys.setrecursionlimit(50000)    # adjust numbers
# threading.stack_size(134217728)   # for your needs

# main_thread = threading.Thread(target=main)
# main_thread.start()
# main_thread.join()

async def init():
    start = time.time()
    BASE_ADDRESS = 'http://192.168.3.213:5000'
    path_api = 'Temperature'
    sub_area = '/date'
    path_variables = '?LoadDate=2023-08-24T00:00:00'
    #x = requests.get('https://h4motion.victorkrogh.dk/api/v1/device/sessions/8EC325DE-A87F-43F5-B1B8-69437593895B/humidity')
    #x = await requests.get(f'{BASE_ADDRESS}/{path_api}')
    x = await requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
    data_json = x.content
    # print(data_json)
    data = json.loads(data_json)
    # print(data["Temperature"])
    df = pd.DataFrame(data["Temperature"])
    del df["ID"]
    # del df["deviceSessionId"]
    # del df["humidityPercentage"]
    # del df["created"]
    # del df["modified"]


    # Convert 'LoadDate' column to LoadDatetime type
    df['LoadDate'] = pd.to_datetime(df['LoadDate'])
    # Set 'LoadDate' as the index
    df.set_index('LoadDate', inplace=True)

    # Plot the data
    plt.figure(figsize=(12, 8))
    #plt.switch_backend('agg')
    plt.plot(df.index, df['Temperature'])

    plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    plt.gca().xaxis.set_major_locator(mLoadDates.MinuteLocator(interval=250))

    plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

    plt.title('Temperature over Time')
    plt.xlabel('LoadDate')
    plt.ylabel('Temperature')
    stop = time.time()
    print(stop - start)
    #plt.show()

import io
import base64


async def plot_to_img():
    start = time.time()
    await init()
    img = io.BytesIO()
    plt.savefig(img,format='jpg')
    img.seek(0)

    img_b64 = base64.b64encode(img.getvalue()).decode()
    if img:
        del img
    return img_b64

#asyncio.run(plot_to_img())

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

