import sqlite3
from bs4 import BeautifulSoup
import requests
from sklearn.decomposition import sparse_encode
import json
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

    def getMovies(self):
        """Updates the movies.bd"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Movies(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITLE TEXT NOT NULL,
                ORIGINAL_TITLE TEXT,
                COUNTRY TEXT,
                SPAIN_DATE DATE,
                DIRECTOR TEXT,
                GENRE TEXT
            );"""
        )
        visited = set()
        for elem in self.soup.select('a[href^="/peliculas/"][href$=".html"]'):
            url_movie = "https://www.elseptimoarte.net" + elem["href"]
            if url_movie in visited:
                continue
            visited.add(url_movie)
            movie = self.get_movie(url_movie)
            print(movie)
            # return f"insert into movies values({title}, {original_title},\
        #      {country}, date('{spain_date}'), {director}, {genre})"
        # cursor.execute(movie)
        # https://stackoverflow.com/questions/20444155/python-proper-way-to-store-list-of-strings-in-sqlite3-or-mysql
        #  CAMBIAR GENRE Y DIRECTOR Y PAIS A LISTA DE STR Y FORMATEAR ENTRADA

    def get_movie(self, url_movie: str) -> str:
        """Takes an url and and index and returns the movie in the url"""
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

        movie = {
            "TITLE": title,
            "ORIGINAL_TITLE": original_title,
            "COUNTRY": country,
            "SPAIN_DATE": f'date("{spain_date}")',
            "DIRECTOR": director,
            "GENRE": genre,
        }

        return json.dumps(movie)


scrapper = Scrapper("https://www.elseptimoarte.net/estrenos/", "movies.db")
scrapper.getMovies()

# json.loads(movie) para parsear a dict
