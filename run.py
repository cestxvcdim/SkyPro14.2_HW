from flask import Flask, request, render_template
from utils import *

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/movie/title')
def movie_title_page():
    title = request.args.get('title')
    movie = search_by_title(title)
    return render_template('movie_title_page.html', movie=movie)


@app.route('/movie/year_to_year')
def movies_release_year_page():
    from_year = request.args.get('from_year')
    to_year = request.args.get('to_year')
    movies = search_by_years(int(from_year), int(to_year))
    return render_template('movies_release_year_page.html', movies=movies)


@app.route('/rating/<rating>')
def rating_page(rating):
    if rating == 'children':
        rating = ('G', 'TV-G')
    elif rating == 'family':
        rating = ('G', 'PG', 'PG-13')
    elif rating == 'adult':
        rating = ('R', 'NC-17')
    movies = search_by_rating(rating)
    return render_template('movies_rating_page.html', movies=movies)



@app.route('/genre/genre')
def movie_genre_page():
    genre = request.args.get('genre')
    movies = search_by_genre(genre)
    return render_template('movies_genre_page.html', movies=movies)


@app.errorhandler(404)
def not_found_page(e):
    return '<h1>404 Error</h1>'


@app.errorhandler(500)
def internal_server_page(e):
    return '<h1>500 Error</h1>'

if __name__ == '__main__':
    app.run()
