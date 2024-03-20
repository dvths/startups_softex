import scrapy


class StartupsSpider(scrapy.Spider):
    name = 'startups'
    start_urls = ['https://softexpe.org.br/']

    # Requisição para a página de catálogo a partir do URL inicial
    def parse(self, response):

        catolog_link = response.xpath(
            '//nav//li[@id="menu-item-3583"]/a[re:test(@href, "catalogo")]/@href'
        ).get()

        yield scrapy.Request(catolog_link, callback=self.parse_catalog)


    def parse_catalog(self, response):
        # Obtem os URLs relativos a cada card que representa uma empresa
        relative_urls = response.xpath(
            '//div[@class="listing_box"]/a[re:test(@href, "catalogo")]/@href'
        ).getall()

        # Itera pela lista de cards para extração das informações
        for relative_url in relative_urls:
            yield scrapy.Request(
                response.urljoin(relative_url), callback=self.extract_data
            )

        # Obtem os URLs das págincas que contém cards
        pages = response.xpath(
            '//div[@class="pagination"]//div[@class="pagination_ids"]/a/@href'
        ).getall()

        # Itera por cada página para manter o ciclo de análise e extração
        for page in pages:
            yield scrapy.Request(
                response.urljoin(page), callback=self.parse_catalog
            )

    def extract_data(self, response):
        # Mapeamento para cada informação desejada para extração
        startup_name = ' '.join(
            response.xpath('//div[@class="col-details"]/p/text()')
            .get()
            .split()
        )

        startup_contact = response.xpath(
            '//div[@class="col-content"]/a[@class="contact-card"][1]/text()'
        ).get()

        startup_email = response.xpath(
            '//div[@class="col-content"]/a[@class="contact-card"][2]/text()'
        ).get()
        startup_website = response.xpath(
            '//div[@class="col-content"]/a[@class="contact-card"][3]/text()'
        ).get()
        startup_address = ' '.join(
            response.xpath(
                '//div[@class="col-content"]/a[@class="contact-card"][4]/text()'
            )
            .get()
            .split()
        )
        startup_segment = response.xpath(
            '//div[@class="col-details"]/p[3]/text()'
        ).get()

        startup_metodology = response.xpath(
            '//div[@class="col-details"]/p[5]/text()'
        ).get()
        startup_description = response.xpath(
            '//div[@class="col-details"]/textarea/text()'
        ).get()

        tags = response.xpath('//div[@class="col-details"]/a/text()').getall()

        startup_tags = [tag for tag in tags]
        
        yield {
            'STARTUP_NAME': startup_name,
            'STARTUP_CONTACT': startup_contact,
            'STARTUP_EMAIL': startup_email,
            'STARTUP_WEBSITE': startup_website,
            'STARTUP_ADDRESS': startup_address,
            'STARTUP_SEGMENT': startup_segment,
            'STARTUP_METODOLOGY': startup_metodology,
            'STARTUP_DESCRIPTION': startup_description,
            'STARTUP_TAGS': startup_tags,
        }
