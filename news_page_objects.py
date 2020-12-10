import bs4
import requests
from common import config


class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)
        # metodo que sale error si la solicitud no es enviada correctamente.
        response.raise_for_status()
        # importa el texto de la variable response parseada con bs4  a el metodo _html
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):    # clase de pagina principal
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
        
    @property #def dentro de un def
    def article_links(self):
        link_list=[]
        # itera en los queries que estan con atributo CSS definido en confing.yaml los guarda en la variable link
        for link in self._select (self._queries["homepage_article_links"]):
            # si la vairble link tiene el atributo href entonces la agrega a la lista que tenemos vacia y que creamos
            if link and link.has_attr("href"):
               link_list.append(link)

        # hace un set (es decir quita los duplicados) queremos la propiedad href por cada link en la lista de links
        return set(link["href"] for link in link_list)



class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''

