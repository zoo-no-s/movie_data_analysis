# 환경세팅
import requests
from datetime import date, datetime, timedelta

import os
from dotenv import load_dotenv

import pandas as pd

load_dotenv()
APIKEY = os.getenv('KOBIS_API_KEY')
URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'

# day_ago_list = range(1, 15) # 1일 전부터 14일전까지
day_ago_list = range(1, 2) # 1일 전

for day_ago in day_ago_list : 
    target_date = (date.today() - timedelta(days=day_ago))

    params = {
        'key': APIKEY,
        'targetDt' : target_date.strftime("%Y%m%d")
    }

    response = requests.get(URL, params=params, timeout=30)
    movie_info_list = response.json()["boxOfficeResult"]["dailyBoxOfficeList"]

    movie_list = []

    for movie_info in movie_info_list :
        movie_info['b_date'] = target_date.strftime("%Y-%m-%d")
        movie_info['c_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del movie_info['rnum']
        movie_list.append(movie_info)

    pd.DataFrame(movie_list).to_csv(f'../data/raw/movie_info_api/movie_info_api_{target_date.strftime("%Y%m%d")}.csv', index=False, encoding='utf-8-sig')