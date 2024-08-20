import urllib.request
from pprint import pprint
import json
import csv

API_KEY = f"{"3241b215148b936b9f2f9fedf09f9c34"}"
HOST = "https://api.themoviedb.org"
MOVIE_LIST_URI = "/3/movie/popular"
MOVIE_INFO_URI = "/3/movie/"
GENRE_LIST_URI = "/3/genre/movie/list"

movie_list = []
movie_Ids = []
genre_list = []

# 장르 데이터 가져오기
genre_request = (f'{HOST}{GENRE_LIST_URI}?api_key={API_KEY}&language=ko')
response = urllib.request.urlopen(genre_request)
json_str = response.read().decode('utf-8')
json_object = json.loads(json_str)

genre_data = json_object.get("genres")

for data in genre_data:

    my_data = {
        "number": data.get("id"),
        "name": data.get("name")
    }

    my_genre = {
        "model": "movies.genre",
        "pk": my_data.get("number"),
        "fields": {
            "name": my_data.get("name")
        },
    }
    genre_list.append(my_genre)

# 영화 ID 가져오기
for i in range(1, 50):
    request = (f'{HOST}{MOVIE_LIST_URI}?api_key={API_KEY}&language=ko&page={i}')
    response = urllib.request.urlopen(request)
    json_str = response.read().decode('utf-8')
    json_object = json.loads(json_str)

    data_movies = (json_object.get("results"))

    for movie in data_movies:
        movie_Ids.append(movie.get("id"))

# 영화 세부 정보 가져오기
for idx, movie_Id in enumerate(movie_Ids):
    movie_request = (f'{HOST}{MOVIE_INFO_URI}{movie_Id}?api_key={API_KEY}&language=ko&')
    response = urllib.request.urlopen(movie_request)
    json_str = response.read().decode('utf-8')
    json_object = json.loads(json_str)
    if json_object.get("poster_path"):
        if json_object.get("genres"):

            my_object = {
                "model": "movies.movie",
                "pk": idx+1,
                "fields": {
                    "title": json_object.get("title"),
                    "adult": json_object.get("adult"),
                    "popularity": json_object.get("popularity"),
                    "poster_path": json_object.get("poster_path"),
                    "release_date": json_object.get("release_date"),
                    "runtime": json_object.get("runtime"),
                    "vote_average": json_object.get("vote_average"),
                    "vote_count": json_object.get("vote_count"),
                    "overview": json_object.get("overview"),
                    "genres": [json_object.get("genres")[0].get("id")],
                    "original_title": json_object.get("original_title"),
                }  
            }
        else:
            my_object = {
                "model": "movies.movie",
                "pk": idx+1,
                "fields": {
                    "title": json_object.get("title"),
                    "adult": json_object.get("adult"),
                    "popularity": json_object.get("popularity"),
                    "poster_path": json_object.get("poster_path"),
                    "release_date": json_object.get("release_date"),
                    "runtime": json_object.get("runtime"),
                    "vote_average": json_object.get("vote_average"),
                    "vote_count": json_object.get("vote_count"),
                    "overview": json_object.get("overview"),
                    "genres": json_object.get("genres"),
                    "original_title": json_object.get("original_title"),
                }
            }
        movie_list.append(my_object)

# JSON 파일 저장
with open('movies.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(movie_list, ensure_ascii=False))

with open('genres.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(genre_list, ensure_ascii=False))

# CSV 파일 저장 추가
# 영화 데이터를 CSV로 저장
try:
    with open('movies.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = ['title', 'adult', 'popularity', 'poster_path', 'release_date', 'runtime', 'vote_average', 'vote_count', 'overview', 'genres', 'original_title']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for movie in movie_list:
            fields = movie['fields']
            genres = ','.join(str(g) for g in fields['genres'])
            writer.writerow({
                'title': fields['title'],
                'adult': fields['adult'],
                'popularity': fields['popularity'],
                'poster_path': fields['poster_path'],
                'release_date': fields['release_date'],
                'runtime': fields['runtime'],
                'vote_average': fields['vote_average'],
                'vote_count': fields['vote_count'],
                'overview': fields['overview'],
                'genres': genres,
                'original_title': fields['original_title']
            })
    print("movies.csv written successfully.")
except Exception as e:
    print(f"Error writing movies.csv: {e}")

# 장르 데이터를 CSV로 저장
try:
    with open('genres.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for genre in genre_list:
            fields = genre['fields']
            writer.writerow({
                'id': genre['pk'],
                'name': fields['name']
            })
    print("genres.csv written successfully.")
except Exception as e:
    print(f"Error writing genres.csv: {e}")
