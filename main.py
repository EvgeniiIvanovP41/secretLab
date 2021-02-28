import requests
import sched
import time
from datetime import datetime, timezone
from influxdb import InfluxDBClient

dataBaseName = 'myDataBase'
influxURL = 'http://192.168.26.128:8086'

headers = {
    'format': 'application/json',
    'type': 'application/x-www-form-urlencoded',
    'coding': 'gzip'
}


def getInfoAboutCryptocurrency():
    req = requests.get(
        'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL')
    print(req)
    return req


def createDataBase():
    client = InfluxDBClient(host='192.168.26.128', port=8086)
    client.create_database(dataBaseName)


def parseData(lists):
    line = ''
    for list in lists:
        if(list[0][0] == 't'):
            symbol, bid, bidSize, ask, askSize, dailyChange, dailyChangeRelative, lastPrice, volume, high, low = list
            line += f'{dataBaseName},pair={symbol} bid={bid},bid_size={bidSize},ask={ask},ask_size={askSize},daily_change={dailyChange},daily_change_rel={dailyChangeRelative},last_price={lastPrice},volume={volume},high={high},low={low}\n'
    return line


def writeData(receivedData):
    influxWrite = influxURL + '/write?' + 'db=' + dataBaseName + '&precision=s'
    req = requests.post(influxWrite, headers=headers, data=receivedData)
    return req


while True:
    getData = getInfoAboutCryptocurrency()
    createDataBase()
    parseResult = parseData(getData.json())
    recording = writeData(parseResult)
    time.sleep(10)
