"""
Provides some repetitive or formatting functionalities
"""


def format_list(text: str, separator: str) -> list:
    """Takes a comma separated string of items and returns
    a list with those"""
    return list(map(lambda x: x.strip().replace("'", ""), text.split(separator)))


def format_movies(results: list) -> dict:
    """Takes the output of the JOIN and organizes all the films
    with theit data"""
    titles = sorted(list({movie[0] for movie in results}))
    i = 0
    title = titles[i]
    movies = {title: [set(), set()]}
    for data in results:
        if data[0] == title:
            movies[title][0].add(data[1])
            movies[title][1].add(data[2])
        elif i + 1 < len(titles):
            title = titles[i + 1]
            movies[title] = [set(), set()]
            movies[title][0].add(data[1])
            movies[title][1].add(data[2])
            i += 1
    return movies
