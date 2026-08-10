# 환경 세팅
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, date
import pandas as pd

# 기본 변수 지정
BASE_URL = 'https://cine21.com/'
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; EducationalScraper/1.0; +https://github.com/zoo-no-s)"
}

# 박스 오피스 상위 10편 영화 정보 가져오기
res = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 타깃 되는 DOM 찾기
a = soup.select_one('.wide_gray_bg_wrap_inner a[href*="movie/rank"]')
parent = a.find_parent(class_='wide_gray_bg_wrap_inner') if a else None
top_10_movie = parent.select('.swiper-slide')

# 수집용 리스트
top_10_movie_info = []
top_10_movie_review = []

# 영화 정보 수집
for movie in top_10_movie:

    # 미개봉작에 대한 예외처리 추가
    rank = movie.select_one('.rank').text
    title = movie.select_one('.title').text 
    score = movie.select_one('.star_wrap .num').text if movie.select_one('.star_wrap .num') else None
    daily_audience = movie.select_one('.etc_info p:nth-child(1)').text.split('명')[0].replace(',','') if movie.select_one('.etc_info p:nth-child(1)') else None
    total_audience = movie.select_one('.etc_info p:nth-child(2)').text.split(':')[1].split('명')[0].replace(',','') if movie.select_one('.etc_info p:nth-child(2)') else None
    release_date = movie.select_one('.etc_info p:nth-child(3)').text.split(':')[1] if movie.select_one('.etc_info p:nth-child(3)') else None
    href = movie.select_one("a").get('href') if movie.select_one("a").get('href') else None


    top_10_movie_info.append({
        'rank' : rank,
        'title' : title,
        'score' : score,
        'daily_audience' : daily_audience,
        'total_audience' : total_audience,
        'release_date' : release_date,
        'href' : href,
    })

# 영화 상세 정보 수집
for movie in top_10_movie_info:
    # 경로에 대한 예외처리 추가
    if(movie['href'] != 'javascript:;') : 

        res = requests.get(f"{BASE_URL}{movie['href']}", headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        id = movie['href'].split('=')[1]
    

        # 데이터 추가 수집
        movie['id'] = id
        movie['genre'] = soup.select_one('.info_list li:nth-child(5)').text.replace(' ', '').replace('\n','')[2:]
        movie['grade'] = soup.select_one('.info_list li:nth-child(2)').text.replace(' ', '').replace('\n','')[2:]
        movie['time'] = soup.select_one('.info_list li:nth-child(3)').text.replace(' ', '').replace('\n','')[2:]
        movie['director'] = soup.select_one('.info_list li:nth-child(8) a').text.replace(' ', '').replace('\n','')
        movie['expert_score'] = soup.select_one('.star_box .star_cine21:first-child .num').text
        movie['nation'] = soup.select_one('.info_list li:nth-child(6)').text.replace(' ', '').replace('\n','')[2:]
        movie['c_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        movie['b_date'] = date.today().strftime("%Y-%m-%d")

        # 리뷰 수집
        review_list = soup.select('.expert_star li')
        for review in review_list :
            top_10_movie_review.append({
                'id' : movie['href'].split('=')[1],
                'reviewer_name' : review.select_one('.reviewer .name').text,
                'score' : review.select_one('.reviewer .num').text,
                'review' : review.select_one('.review').text,
                'c_datetime' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'b_date' : date.today().strftime("%Y-%m-%d")
            })
            
        # 서버 과부하를 막기 위한 에티켓
        time.sleep(1)

# csv 추출
pd.DataFrame(top_10_movie_info).to_csv(f'../data/raw/movie_info_scrap/movie_info_scrap_{date.today().strftime("%Y%m%d")}.csv', index=False, encoding='utf-8-sig')
pd.DataFrame(top_10_movie_review).to_csv(f'../data/raw/movie_review_scrap/movie_review_scrap_{date.today().strftime("%Y%m%d")}.csv', index=False, encoding='utf-8-sig')