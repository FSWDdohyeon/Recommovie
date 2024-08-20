import csv
import requests

# TheMovieDB API 키
api_key = "3241b215148b936b9f2f9fedf09f9c34"

# 헤더 설정
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# CSV 파일로부터 영화 제목 읽기
input_filename = "movie_titles.csv"
movie_titles = []

with open(input_filename, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # Assume that the first column in the CSV contains the movie titles
        movie_titles.append(row[0])

# 각 영화 제목에 대해 API 호출
for title in movie_titles:
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page=1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        # 결과 처리
        if data['results']:
            movie = data['results'][0]
            movie_title = movie['title']
            overview = movie['overview']
            release_date = movie['release_date']
            print(f"Title: {movie_title}\nOverview: {overview}\nRelease Date: {release_date}\n")
        else:
            print(f"No results found for '{title}'.")
    else:
        print(f"Error: Unable to fetch data for '{title}'. Status code: {response.status_code}")
