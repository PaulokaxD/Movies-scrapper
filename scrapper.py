import sqlite3
from bs4 import BeautifulSoup
import requests
import funcionalities


class Scrapper:
    """Get the new movies in the elseptimoarte.net webpage and
    stores them into a database"""

    cursor: sqlite3.Cursor
    soup: BeautifulSoup
    connection: sqlite3.Connection

    def __init__(self, url: str, db: str) -> None:
        conn = sqlite3.connect(db)
        html_doc = requests.get(url)

        self.connection = conn
        self.cursor = conn.cursor()
        self.soup = BeautifulSoup(html_doc.content, "html.parser")

    def init_tables(self) -> None:
        """Creates all tables if necessary"""

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Movies(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                original_title TEXT,
                spain_date DATE);"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Countries(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                country TEXT,
                FOREIGN KEY (movie_id) REFERENCES Movies(id));"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Directors(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                director TEXT,
                FOREIGN KEY (movie_id) REFERENCES Movies(id));"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Genres(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                genre TEXT,
                FOREIGN KEY (movie_id) REFERENCES Movies(id));"""
        )

    def update_database(self) -> str:
        """Updates the movies.bd"""

        self.init_tables()

        visited = set()
        for i, elem in enumerate(
            self.soup.select('a[href^="/peliculas/"][href$=".html"]')
        ):
            url_movie = "https://www.elseptimoarte.net" + elem["href"]
            if url_movie in visited:
                continue
            visited.add(url_movie)
            movie_data = self.get_movie(url_movie)
            print("Cargando...")
            self.insert_movie(movie_data, i)
        self.connection.commit()
        self.cursor.execute("SELECT COUNT(*) FROM Movies")
        return self.cursor.fetchone()[0]

    def get_movie(self, url_movie: str) -> list:
        """Takes an url and returns a list with all the needed data
        in the following order:
            title: str, original_title: str, country: list(str),
            spain_date: str, director: list(str), genre: list(str)
        """
        movie_page = requests.get(url_movie)
        movie_soup = BeautifulSoup(movie_page.content, "html.parser")
        for element in movie_soup.select("*"):
            if element.name == "dl":
                info = funcionalities.format_list(element.text, "\n")
                for i, fact in enumerate(info):
                    if fact == "Título":
                        title = info[i + 1]
                    elif fact == "Título original":
                        original_title = info[i + 1]
                    elif fact == "Estreno en España":
                        auxiliar_date = funcionalities.format_list(info[i + 1], "/")
                        spain_date = (
                            f"{auxiliar_date[2]}-{auxiliar_date[1]}-{auxiliar_date[0]}"
                        )

                    elif fact == "País":
                        country = funcionalities.format_list(info[i + 1], ",")
            else:
                clases = element.attrs.get("class")
                clases = clases if clases is not None else []
                if "categorias" in clases:
                    genre = funcionalities.format_list(element.text, ",")
                elif "director" in clases:
                    director = funcionalities.format_list(element.text, ",")

        return [title, original_title, country, spain_date, director, genre]

    def insert_movie(self, movie_data: list, i: int) -> None:
        """Takes the list with all the needed extracteed data about a movie
        and inserts the film in the movies.db"""

        self.cursor.execute(
            f"INSERT INTO Movies(title, original_title, spain_date) VALUES\
        ('{movie_data[0]}', '{movie_data[1]}', date('{movie_data[3]}'))"
        )
        for country in movie_data[2]:
            self.cursor.execute(
                f"INSERT INTO Countries(movie_id, country)\
             VALUES ('{i}', '{country}')"
            )
        for director in movie_data[4]:
            self.cursor.execute(
                f"INSERT INTO Directors(movie_id, director)\
             VALUES ('{i}', '{director}')"
            )
        for genre in movie_data[5]:
            self.cursor.execute(
                f"INSERT INTO Genres(movie_id, genre)\
             VALUES ('{i}', '{genre}')"
            )

    def show_movies(self) -> dict:
        """Returns a dictionary where the key is the movies' name
        and the values are two sets with the countries and directors"""

        self.cursor.execute(
            """SELECT Movies.title, Countries.country,Directors.director
            FROM Movies
            INNER JOIN Countries
            ON Countries.movie_id = Movies.id
            INNER JOIN Directors
            ON Directors.movie_id = Movies.id
            ORDER BY Movies.title"""
        )
        results = self.cursor.fetchall()
        movies = funcionalities.format_movies(results)
        return movies
