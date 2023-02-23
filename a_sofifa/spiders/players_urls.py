import logging
import scrapy

class ASofifaSpider(scrapy.Spider):
	name='players_urls'

	def __init__(self):
		self.pages = 0

	def start_requests(self):
		urls = [
			'https://sofifa.com/players?col=oa&sort=desc&offset=0'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		logging.info(self.pages)
		for player in response.css('.col-name'):
			player_links = player.xpath('a/@href').re(r'/player/\w+')
			if len(player_links) > 0:
				yield {
					'player_url': player_links[0]
				}

		offset = response.url[51:]
		logging.info('************************************ ' + 'offset is ' + str(offset))
		end_offset = 1

		# These offsets dont have next buttons. Fk em
		# bad_offsets = [360, 1020, 1440, 1620, 1680, 1920, 2220, 2340, 2400]

		if int(offset) <= end_offset:
			next_href = '/players?col=oa&sort=desc&offset=' + str(int(offset)+60)
			next_page_url = 'https://sofifa.com' + next_href
			self.pages += 1
			request = scrapy.Request(url=next_page_url)
			yield request
