import csv
import requests

# TheMovieDB API 키
api_key = "3241b215148b936b9f2f9fedf09f9c34"

# 헤더 설정
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMjQxYjIxNTE0OGI5MzZiOWYyZjlmZWRmMDlmOWMzNCIsIm5iZiI6MTcyMzExMDQ0MC4yNTczMjIsInN1YiI6IjY2YjJjZmE5NzY5MDJmOTYyY2I1MTViOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NkJcTzq4Lfd-Yr_Ptsvfi4l2CDZ1sGByyNykNfaQodM"
}
def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['genre_ids'][0]
        else:
            print(f"No results found for '{title}'.")
            return None
    else:
        print(f"Error: Unable to fetch data for '{title}'. Status code: {response.status_code}")
        return None

def find_movies_by_id(input_filename, movie_id):
    matched_movies = []
    
    with open(input_filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row['genres'] == str(movie_id):
                matched_movies.append(row)
    
    return matched_movies

 


def main():
    # 사용자가 입력한 영화 제목
    movie_title = input("Enter the movie title: ")

    # 영화 검색을 통해 영화 ID를 가져옴
    movie_id = search_movie(movie_title)
    
    if movie_id:
        # 영화 ID로 CSV 파일에서 해당 영화를 찾음
        input_filename = "movies.csv"
        matched_movies = find_movies_by_id(input_filename, movie_id)
        
        if matched_movies:
            print(f"Movies found with ID {movie_id}:")
            for movie in matched_movies:
                print(f"Title: {movie['title']}, Release Date: {movie['release_date']}, Overview: {movie['overview']}")
        else:
            print(f"No movies found with ID {movie_id}.")

if __name__ == "__main__":
    main()
