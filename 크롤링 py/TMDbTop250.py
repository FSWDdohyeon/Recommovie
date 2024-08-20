# ===== import ===== #

# selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# 로그
import logging

# 그외 기본 모듈
import csv
import os 
import time

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.info("크롤링 시작")

# ===== 셀레니움 설정 ===== #
headless = True
header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# chrome driver option 생성
driver_option = webdriver.ChromeOptions()

# Selenium headless 설정
if headless:
    driver_option.add_argument("--headless")

# Selenium Option 설정
options = {
    'disable_gpu': 'disable-gpu',
    'lang': 'lang=ko_KR',
    'User_Agent': f'user-agent={header}',
    'window-size': '1920x1080'
}

for i in options.values():
    driver_option.add_argument(i)

# 불필요한 에러 메세지 삭제
driver_option.add_experimental_option("excludeSwitches", ["enable-logging"])
driver_option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver_option.add_experimental_option('useAutomationExtension', False)

# 크롬 드라이버 버전 설정: 버전명시 안하면 최신
service = ChromeService(ChromeDriverManager().install())

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=service, options=driver_option) 

# IMDb 웹 페이지 열기
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
driver.get(url)

# 페이지가 로드될 때까지 잠시 기다립니다.
time.sleep(5)

# 스크롤하여 페이지 끝까지 이동합니다.
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지를 아래로 스크롤합니다.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 페이지 로드가 완료되도록 잠시 기다립니다.
    time.sleep(2)
    
    # 새로운 높이를 가져옵니다.
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # 페이지 끝까지 도달했는지 확인합니다.
    if new_height == last_height:
        break
    
    last_height = new_height


# CSV 파일을 설정합니다.
filename = "TOP250.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

# CSV 파일의 헤더를 작성합니다.
attributes = ["image", "title", "rate", "data"]
writer.writerow(attributes)

TopRanking = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

for Top250 in TopRanking:
    try:
        image = Top250.find_element(By.TAG_NAME, 'img').get_attribute('src')
        title = Top250.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
        rate = Top250.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text
        data = Top250.find_element(By.CSS_SELECTOR, "div.sc-b189961a-7").text
        data_rows = [image, title, rate, data]
        writer.writerow(data_rows)
    except Exception as e:
        print(f"Error: {e}")

# 브라우저를 닫습니다.
driver.quit()
f.close()
