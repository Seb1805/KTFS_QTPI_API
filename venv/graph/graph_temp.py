
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
import gc
import datetime
import os
from dotenv import load_dotenv as denv

denv()

mplstyle.use('fast')
async def main(path_api, y_akse = None):
    img = await plot_to_img(path_api, y_akse)
    return img


async def init(path_api, y_akse):
    BASE_ADDRESS = f'http://{os.getenv("SERVER_IP")}:{os.getenv("PORT")}'
    # path_api = 'Temperature'
    sub_area = '/date'
    currentDate = datetime.datetime.now()
    weekago = currentDate - datetime.timedelta(days=7)
    
    path_variables = f'?StartDate={weekago.strftime("%Y-%m-%d")}T00:00:00&EndDate={currentDate.strftime("%Y-%m-%dT%H:%M:%S")}'

    x = await requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')

    data_json = x.content

    data = json.loads(data_json)

    df = pd.DataFrame(data[path_api])
    del df["ID"]


    # Convert 'LoadDate' column to Datetime type
    df['LoadDate'] = pd.to_datetime(df['LoadDate'])
    # Set 'LoadDate' as the index
    df.set_index('LoadDate', inplace=True)

    # Plot the data
    plt.figure(figsize=(10, 6))
    if(y_akse == None):
        plt.plot(df.index, df[path_api])
    else:
        plt.plot(df.index, df[y_akse])
    plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%m/%d %H:%M:%S'))

    plt.gca().xaxis.set_major_locator(mLoadDates.HourLocator(interval=12))

    plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

    plt.title(f'{path_api} over Time')
    plt.xlabel('Date and time')
    if(y_akse == None):
        plt.ylabel(path_api)
    else:
        plt.ylabel(y_akse)
    stop = time.time()
    gc.collect() # collect the trash



import io
import base64


async def plot_to_img(path_api, y_akse):
    await init(path_api, y_akse)
    img = io.BytesIO()
    plt.savefig(img,format='jpg')
    img.seek(0)

    img_b64 = base64.b64encode(img.getvalue()).decode()
    if img:
        del img #remove ref
        gc.collect() #collect the trash
    return img_b64

#Used to run funtion synchronically > used for test purposes
#asyncio.run(plot_to_img())

