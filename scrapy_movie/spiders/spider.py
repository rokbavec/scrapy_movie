from scrapy import Spider
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy_movie.items import MovieItem


class MovieSpider(Spider):
    """
    Spider, ki iz spletne strani http://movieweb.com/ pobere vse filme, ki izidejo v letu 2016. O filmu
    pridobimo naslednje podatke: naslov, opis, zanr, direktorja, url, url slike, datum izida.
    """
    name = "movie"
    allowed_domains = ["movieweb.com"]
    start_urls = settings['START_URLS']

    def parse(self, response):
        """
        Metoda sprva pridobi vse povezave do filmov, in nato za vsak url(film) klice funkcijo za pridobivanje podatkov o filmu.
        """
        sel = Selector(response)

        """
        Pridobimo seznam url-jev filmov.
        """
        url_list = sel.xpath('//div[@class="movies-list"]/div[@class="media movie-item"]/div[@class="media-body"]/h2/a/@href').extract()

       
        """
        Za vsak url posebej klicemo metodo parse_movies, ki pridobiva podatke o filmu iz podanega url-ja.
        """
        for movie_url in url_list:
            yield Request(movie_url, callback=self.parse_movies)

    def parse_movies(self, response):
        """
        Metoda parsa podatke o filmu s strani iz url-ja, ki ga prej pridobimo.
        """
        sel = Selector(response)

        """
        Kreiranje objekta za shranjevanje pridobljenih podatkov o filmu.
        """
        item = MovieItem()
        """
        Klic metod, ki pridobivajo podatke o filmu.
        """
        item['name'] = self.get_movie_name(sel)
        item['description'] = self.get_description(sel)
        item['director'] = self.get_director(sel)
        item['img_src'] = self.get_img_src(sel)
        item['released'] = self.get_release_date(sel)
        item['genre'] = self.get_genre(sel)
        item['url'] = response.request.url
        
        return item

    def trim(self, raw_str):
        """
        Odstrani vse nepravilne prazne znake v nizu.
        """
        return raw_str.encode('ascii', errors='ignore').strip()

    def get_movie_name(self, selector):
        """
        Pridobivanje naslova filma.
        """
        movie_name = selector.xpath('//div[@class="intro-content"]/h1/span[@itemprop ="name"]/text()').extract()[0]

        return self.trim(movie_name)

    def get_description(self, selector):
        """
        Pridobivanje opisa filma.
        """
        description = selector.xpath('//span[@class="summary"]/p/text()').extract()[0]

        return self.trim(description)
    
    def get_director(self, selector):
        """
        Pridobivanje imena direktorja filma.
        """
        director = selector.xpath('//div[@class="col-md-4"]/ul[@class="details"]/li[@class="media"]/div[@class="media-body"]/a/span[@itemprop="name"]/text()').extract()[0]

        return self.trim(director)
    
    def get_img_src(self, selector):
        """
        Pridobivanje url slike filma.
        """
        img_src = selector.xpath('//div[@class="featured-art"]/a/img[@itemprop="image"]/@src').extract()[0]

        return self.trim(img_src)

    def get_release_date(self, selector):
        """
        Pridobivanje datuma izida filma.
        """
        release_date = selector.xpath('//div[@class="col-md-4"]/ul[@class="details"]/li[@class="media"]/div[@class="media-body"]/a/text()').extract()[0]

        return self.trim(release_date)
    
    def get_genre(self, selector):
        """
        Pridobivanje zanra filma.
        """
        genre = selector.xpath('//div[@class="intro-content"]/nav[@class ="intro-nav"]/ul/li/a/text()').extract()[0]

        return self.trim(genre)
    
