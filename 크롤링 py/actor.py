import csv
import requests
from bs4 import BeautifulSoup

filename = "dateMovie.csv"
with open(filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    attributes = ["제목", "예매율", "개봉일", "포스터"]
    writer.writerow(attributes)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    url = "https://www.megabox.co.kr/movie"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 영화 목록 추출 (class="no-img" 요소 찾기)
    items = soup.find_all("li", class_="no-img")

    for item in items:
        title_tag = item.find('p', class_='tit')
        rate_tag = item.find('span', class_='rate')
        release_date_tag = item.find('span', class_='date')
        img_tag = item.find('img', class_='poster')

        title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
        saleRate = rate_tag.get_text(strip=True) if rate_tag else "Unknown Sale Rate"
        release_date = release_date_tag.get_text(strip=True) if release_date_tag else "Unknown Release Date"
        img = img_tag['src'] if img_tag else "No Image"

        data_rows = [title, saleRate, release_date, img]
        writer.writerow(data_rows)

print(f"정보가 '{filename}' 파일에 저장되었습니다.")
