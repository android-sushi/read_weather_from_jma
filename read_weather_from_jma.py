import pprint
import requests
from datetime import datetime


def parse_date(get_data):
    row_date = datetime.strptime(get_data, '%Y-%m-%dT%H:%M:%S%z')
    show_date = row_date.strftime('%Y年%#m月%#d日%H時')
    return show_date


def parse_three_date(get_data, name):
    return_data = {name: get_data}
    index = 0
    for data in return_data[name]:
        try:
            return_data[name][index] = parse_date(data)
        except ValueError:
            return_data[name][index] = ' '.join(data.split())
        index += 1
    return return_data


def main():
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/040000.json"
    header = {"content-type": "application/json"}

    response = requests.get(url, headers=header)
    data = response.json()

    publishing_office = data[0]['publishingOffice']    # 仙台管区気象台
    report_datetime = parse_date(data[0]['reportDatetime'])    # 発表日時
    area = data[0]['timeSeries'][0]['areas'][0]['area']['name']    # 場所。今回は仙台市東部のみ
    three_dates = parse_three_date(data[0]['timeSeries'][0]['timeDefines'], 'three_dates')    # 3日間の日付
    three_weathers = parse_three_date(data[0]['timeSeries'][0]['areas'][0]['weathers'], 'three_weathers')    # ３日間の天気

    print(publishing_office, report_datetime, area)
    pprint.pprint(three_dates)
    pprint.pprint(three_weathers)


if __name__ == '__main__':
    main()
