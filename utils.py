import sqlite3


def search_by_title(title: str) -> dict[str, str | int]:
    with sqlite3.connect("database/netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = """
        SELECT title, country, release_year, listed_in, description 
        FROM netflix 
        WHERE title LIKE ? 
        ORDER BY date_added DESC 
        LIMIT 1
        """
        result = cursor.execute(sqlite_query, ('%' + title + '%',)).fetchone()
        return {
            "title": result[0],
            "country": result[1],
            "release_year": result[2],
            "genre": result[3],
            "description": result[4].strip()
        }


def search_by_years(f_year: int, t_year: int) -> list[dict[str, str | int]]:
    with sqlite3.connect("database/netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = """
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN ? AND ?
        LIMIT 100
        """
        result = cursor.execute(sqlite_query, (f_year, t_year)).fetchall()
        movies = []
        for row in result:
            dict_ = {
                "title": row[0],
                "release_year": row[1]
            }
            movies.append(dict_)
        return movies



def search_by_rating(rating: str):
    with sqlite3.connect("database/netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN {rating}
        LIMIT 20
        """
        result = cursor.execute(sqlite_query).fetchall()
        movies = []
        for row in result:
            dict_ = {
                "title": row[0],
                "rating": row[1],
                "description": row[2]
            }
            movies.append(dict_)
        return movies


def search_by_genre(genre: str) -> list[dict[str, str | int]]:
    with sqlite3.connect("database/netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = """
        SELECT title, description
        FROM netflix
        WHERE listed_in LIKE ?
        ORDER BY release_year DESC
        LIMIT 10
        """
        result = cursor.execute(sqlite_query, ('%' + genre + '%',)).fetchall()
        movies = []
        for row in result:
            dict_ = {
                "title": row[0],
                "description": row[1]
            }
            movies.append(dict_)
        return movies


def get_actors(actor1: str, actor2: str) -> list[str]:
    with sqlite3.connect("database/netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        sqlite_query = """
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE ? AND "cast" LIKE ?
        GROUP BY "cast"
        """
        result = cursor.execute(sqlite_query, ('%' + actor1 + '%', '%' + actor2 + '%')).fetchall()
        actors = []
        dict_ = {}
        for row in result:
            for actor_names in row:
                for i in actor_names.split(', '):
                    dict_[i] = 0
        for row in result:
            for actor_names in row:
                for i in actor_names.split(', '):
                    dict_[i] += actor_names.count(i)
        for k, v in dict_.items():
            if k != actor1 and k != actor2:
                if v > 2:
                    actors.append(k)
        return actors



def get_movies_by_chars(type_: str, release_year: int, genre: str) -> list[str]:
    with sqlite3.connect("database/netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = """
        SELECT title
        FROM netflix
        WHERE type = ? AND release_year = ? AND listed_in LIKE ?
        LIMIT 20
        """
        result = cursor.execute(sqlite_query, (type_, release_year, '%' + genre + '%')).fetchall()
        print(result)
        return [row[0] for row in result]
