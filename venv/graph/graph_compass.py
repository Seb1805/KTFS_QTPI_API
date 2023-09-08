
import requests #used to make api call
import json #json lib
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mLoadDates
import matplotlib.style as mplstyle

mplstyle.use('fast')
async def main():
    img = await plot_to_img()
    return img


async def init():

    BASE_ADDRESS = 'http://192.168.3.213:5000'
    path_api = 'Compass'
    sub_area = '/date'
    path_variables = '?LoadDate=2023-08-24T00:00:00'
    x = requests.get(f'{BASE_ADDRESS}/{path_api}{sub_area}{path_variables}')
    data_json = x.content
    data = json.loads(data_json)
    df = pd.DataFrame(data["Compass"])
    del df["ID"]

    # Convert 'LoadDate' column to LoadDatetime type
    df['LoadDate'] = pd.to_datetime(df['LoadDate'])
    # Set 'LoadDate' as the index
    df.set_index('LoadDate', inplace=True)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['DegreesToNorth'])

    # Format the x-axis to display LoadDates properly

    plt.gca().xaxis.set_major_formatter(mLoadDates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mLoadDates.MinuteLocator(interval=250))

    plt.gcf().autofmt_xdate()  # rotates x-axis labels to fit them better

    plt.title('DegreesToNorth over Time')
    plt.xlabel('LoadDate')
    plt.ylabel('DegreesToNorth')

    plt.show()

import io
import base64


async def plot_to_img():
    await init()
    img = io.BytesIO()
    plt.savefig(img,format='jpg')
    img.seek(0)

    img_b64 = base64.b64encode(img.getvalue()).decode()
    if img:
        del img
    return img_b64
