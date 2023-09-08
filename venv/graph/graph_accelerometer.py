import requests #used to make api call
import json #json lib
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates
import matplotlib.style as mplstyle
import gc
import datetime
import os
from dotenv import load_dotenv as denv

denv()

mplstyle.use('fast')
async def main():
    img = await plot_to_img()
    return img

async def init():

    BASE_ADDRESS = f'http://{os.getenv("SERVER_IP")}:{os.getenv("PORT")}'
    path_api = 'Accelerometer'
    sub_area = '/date'
    currentDate = datetime.datetime.now()
    weekago = currentDate - datetime.timedelta(days=7)

    path_variables = f'?StartDate={weekago.strftime("%Y-%m-%d")}T00:00:00&EndDate={currentDate.strftime("%Y-%m-%dT%H:%M:%S")}'

    x = requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
    data_json = x.content
    data = json.loads(data_json)
    df = pd.DataFrame(data["Accelerometer"])
    del df["ID"]

    # Convert 'LoadDate' column to LoadDatetime type
    df['LoadDate'] = pd.to_datetime(df['LoadDate'])
    # Set 'LoadDate' as the index
    df.set_index('LoadDate', inplace=True)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Roll'], color='red', label='Roll')
    plt.plot(df.index, df['Pitch'], color='green', label='Pitch')
    plt.plot(df.index, df['Yaw'], color='cornflowerblue', label='Yaw')

    # Format the x-axis to display LoadDates properly
    plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%m/%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mLoadDates.HourLocator(interval=12))

    plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

    plt.title('Pitch, roll and yaw over Time')
    plt.xlabel('Date and time')
    plt.ylabel('Pitch,Roll, Yaw')

    plt.legend()  # add a legend to show the color coding

import io
import base64


async def plot_to_img():
    await init()
    img = io.BytesIO()
    plt.savefig(img,format='jpg')
    img.seek(0)

    img_b64 = base64.b64encode(img.getvalue()).decode()
    if img:
        del img #remove ref
        gc.collect() #collect the trash
    return img_b64



