import sqlite3
from bs4 import BeautifulSoup
import requests
import funcionalities


class Scrapper:
    """ooo"""

    cursor: sqlite3.Cursor
    soup: BeautifulSoup

    def __init__(self, url: str, db: str) -> None:
        conn = sqlite3.connect(db)
        html_doc = requests.get(url)

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

    def getMovies(self) -> None:
        """Updates the movies.bd"""

        self.init_tables()

        visited = set()
        for elem in self.soup.select('a[href^="/peliculas/"][href$=".html"]'):
            url_movie = "https://www.elseptimoarte.net" + elem["href"]
            if url_movie in visited:
                continue
            visited.add(url_movie)
            movie_data = self.get_movie(url_movie)
            print(movie_data)
            self.insert_movie(movie_data)

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

    def insert_movie(self, movie_data: list) -> None:
        """Takes the list with all the needed extracteed data about a movie
        and inserts the film in the movies.db"""

        self.cursor.execute(
            f"INSERT INTO Movies(title, original_title, spain_date) VALUES\
        ('{movie_data[0]}', '{movie_data[1]}', date('{movie_data[3]}'))"
        )
        for country in movie_data[2]:
            self.cursor.execute(
                f"INSERT INTO Countries(movie_id, country)\
             VALUES ('{movie_data[0]}', '{country}')"
            )
        for director in movie_data[4]:
            self.cursor.execute(
                f"INSERT INTO Directors(movie_id, director)\
             VALUES ('{movie_data[0]}', '{director}')"
            )
        for genre in movie_data[5]:
            self.cursor.execute(
                f"INSERT INTO Genres(movie_id, genre)\
             VALUES ('{movie_data[0]}', '{genre}')"
            )


scrapper = Scrapper("https://www.elseptimoarte.net/estrenos/", "movies.db")
scrapper.getMovies()
