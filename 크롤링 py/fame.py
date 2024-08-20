import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 영화 차트 페이지 URL
url = "https://m.moviechart.co.kr/rank/realtime/index/image"

# HTTP 요청 헤더
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# HTTP GET 요청
response = requests.get(url, headers=headers)
response.raise_for_status()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, "html.parser")

# 영화 목록 추출 (적절한 태그와 클래스 찾기)
movies = soup.find_all('li', class_='movieBox-item')

base_url = "https://www.megabox.co.kr"

# CSV 파일 작성
filename = f"movie_chart_{datetime.now().strftime('%Y-%m-%d')}.csv"
with open(filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["제목", "예매율", "개봉일", "포스터"])

    # 영화 목록 크롤링
    for movie in movies:
        title_tag = movie.find('div', class_='movie-title')
        saleRate_tag = movie.find('li', class_='ticketing')
        release_date_tag = movie.find('li', class_='movie-launch')
        img_tag = movie.find('img')

        title = title_tag.text.strip() if title_tag else "Unknown Title"
        saleRate = saleRate_tag.text.replace('예매율', '').strip() if saleRate_tag else "Unknown Sale Rate"
        release_date = release_date_tag.text.replace('개봉일', '').strip() if release_date_tag else "Unknown Release Date"
        img = base_url + img_tag['src'] if img_tag else "No Image"

        writer.writerow([title, saleRate, release_date, img])

print(f"영화 차트가 '{filename}' 파일에 저장되었습니다.")
