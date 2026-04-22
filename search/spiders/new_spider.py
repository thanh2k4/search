import scrapy
import re
from search_engine import check_link_exists

class NewSpider(scrapy.Spider):
    name = "new"
    url = "https://vnexpress.net/tag/thien-van-139733"
    index_name = "news"

    def start_requests(self):
        for i in range(1, 6):
            yield scrapy.Request(
                url=f"{self.url}-p{i}",
                callback=self.parse_listpage
            )

    def parse_listpage(self, response):
        article_links = response.css(
            'h2.title-news a::attr(href)'
        ).getall()

        for link in article_links:
            if check_link_exists(link , self.index_name):
                continue
            yield scrapy.Request(
                url=link,
                callback=self.parse_article
            )

    def parse_article(self, response):
        raw_text = "\n".join(
            t.strip()
            for t in response.css('article.fck_detail *::text').getall()
            if t.strip()
        )
        content = re.sub(r'\n\s*\n+', '\n', raw_text)
        item = {
            "title": response.css('h1.title-detail::text').get(default="").strip(),
            "time": response.css('span.date::text').get(),
            "link" : response.url,
            "description": response.css('p.description::text').get(default="").strip(),
            "content": content,
        }
        yield item
    

