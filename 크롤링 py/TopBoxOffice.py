import csv
import requests
from bs4 import BeautifulSoup

filename = "TopBox.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

attributes = ["image", "title", "rate", "data"]
writer.writerow(attributes)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url ="https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht"
res = requests.get(url, headers=headers)
res.raise_for_status()
soup=BeautifulSoup(res.text,"lxml")



TBO=soup.find_all("li", attrs={"class":"ipc-metadata-list-summary-item"})
for TopBox in TBO:
    image=TopBox .find('img')['src']
    title=TopBox .find("h3",attrs={"class":"ipc-title__text"}).get_text()
    boxdate=TopBox .find("ul",attrs={"class":"sc-8f57e62c-0"}).get_text()
    rate=TopBox .find("span",attrs={"class":"ipc-rating-star"}).get_text()
    data_rows=[image, title,boxdate ,rate]
    writer.writerow(data_rows)