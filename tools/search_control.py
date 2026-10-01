import webbrowser
from urllib.parse import quote_plus


class SearchController:

    def google_search(self, query):

        query = query.strip()
        url = "https://www.google.com/search?q=" + quote_plus(query)

        webbrowser.open(url)

        return f"Searching Google for {query}, Sir."

    def youtube_search(self, query):

        query = query.strip()
        url = "https://www.youtube.com/results?search_query=" + quote_plus(query)

        webbrowser.open(url)

        return f"Searching YouTube for {query}, Sir."