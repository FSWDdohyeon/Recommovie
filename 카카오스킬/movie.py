from flask import Flask, request, jsonify
import pandas as pd
import re
from Search import search_movie, find_movies_by_id

app = Flask(__name__)

# Load the actor filmography data
actors_data = pd.read_csv('actors_filmography.csv')

# Load the movie chart data
movies_data = pd.read_csv('movie_chart_2024-08-05.csv')

# Load the Naver movie data
gen_movies_data = pd.read_csv('movies.csv')

# Ensure 예매율 is numeric
movies_data['예매율'] = movies_data['예매율'].str.replace('%', '').astype(float)

# List of actor names for entity recognition
actor_names = actors_data['배우 이름'].unique()


genre_names = gen_movies_data['genres'].unique()



# List of entities for top movies request
top_movies_entities = [
    "최신", "최근", "예매율", "최신 영화", "최근에", "요즘 유행하는",
    "요즘에 개봉한", "개봉", "최신작", "개봉한 영화", "개봉영화",
    "최근 영화", "요즘 영화", "최근영화", "요즘영화", "최근 개봉"
]

@app.route('/api/actorMovies', methods=['POST'])
def getMovies():
    body = request.get_json()
    user_input = body['userRequest']['utterance']
    
    # Extract actor's name from user input using simple entity recognition
    actor_name = None
    for name in actor_names:
        if re.search(name, user_input):
            actor_name = name
            break
    
    if actor_name is None:
        response_text = "죄송합니다, 요청하신 배우의 정보를 찾을 수 없습니다."
    else:
        # Filter the data for the actor
        actor_films = actors_data[actors_data['배우 이름'] == actor_name]
        # Randomly sample 5 films
        if len(actor_films) >= 5:
            random_films = actor_films.sample(n=5)
        else:
            random_films = actor_films
        
        films_list = []
        for index, row in random_films.iterrows():
            film_info = f"제목: {row['제목']}, 평점: {row['평점']}"
            films_list.append(film_info)
        
        response_text = f"{actor_name} 배우의 랜덤 추천 영화 목록:\n" + "\n".join(films_list)
    
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                   }
                ]
        }
    }
    return jsonify(responseBody)

@app.route('/api/getTopMovies', methods=['POST'])
def getTopMovies():
    body = request.get_json()
    user_input = body['userRequest']['utterance']
    
    if any(entity in user_input for entity in top_movies_entities):
        # Sort by 예매율 in descending order
        top_movies = movies_data.sort_values(by='예매율', ascending=False).head(10)
        
        cards = []
        for _, row in top_movies.iterrows():
            card = {
                "title": row['제목'],
                "description": f"예매율: {row['예매율']}%, 개봉일: {row['개봉일']}",
                "thumbnail": {
                    "imageUrl": row['포스터']
                }
            }
            cards.append(card)
        
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": cards
                        }
                      }
                    ]
                }
            }
    else:
        response_text = "올바른 요청을 입력하세요."
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": response_text
                        }
                        }
                    ]
                }   
            }

    return jsonify(responseBody)

@app.route('/api/searchMovie', methods=['POST'])
def searchMovie():
    body = request.get_json()
    user_input = body['userRequest']['utterance']
    
    # Extract the movie title from the user input
    movie_title = user_input.strip()
    
    # Search for the movie genre ID using TheMovieDB API
    movie_id = search_movie(movie_title)  # movie_utils 모듈의 함수 사용
    
    if movie_id:
        # Find movies by genre ID in the CSV file
        matched_movies = find_movies_by_id("movies.csv", movie_id)  # movie_utils 모듈의 함수 사용
        
        if matched_movies:
            movies_list = []
            for movie in matched_movies:
                movie_info = f"Title: {movie['title']}, Release Date: {movie['release_date']}, Overview: {movie['overview']}"
                movies_list.append(movie_info)
            
            response_text = f"Movies found for genre ID {movie_id}:\n" + "\n".join(movies_list)
        else:
            response_text = f"No movies found for genre ID {movie_id}."
    else:
        response_text = f"No genre ID found for the movie title '{movie_title}'."
    
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    }
    return jsonify(responseBody)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

