import scrapy
from scrapy_splash import SplashRequest
from scrapy.item import Item
from scrapy.item import Field
from .MyItems import PerGame, Totals, PerPos

player_id = 0

class PlayerSpider(scrapy.Spider):
	name = "playerScrape"

	start_urls = ["https://www.basketball-reference.com/players/d/duranke01.html"]

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

	def parse(self, response):
		global player_id
		name = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()
		per_game = response.selector.xpath('//table[@id="per_game"]/tbody/tr[@class="full_table"]')
		totals = response.selector.xpath('//table[@id="totals"]/tbody/tr[@class="full_table"]')
		per_pos = response.selector.xpath('//table[@id="per_poss"]/tbody/tr[@class="full_table"]')
		adv = response.selector.xpath('//table[@id="advanced"]/tbody/tr[@class="full_table"]')

		for year in per_game:
			stats = PerGame()
			stats["pid"] = player_id
			stats["name"] = name
			link_fields = ["season","team_id","lg_id"]
			fields = ["age","pos","g","gs","mp_per_g","fg_per_g","fga_per_g","fg_pct","fg3_per_g","fg3a_per_g","fg3_pct","fg2_per_g","fg2a_per_g","fg2_pct",
			"efg_pct","ft_per_g","fta_per_g","ft_pct","orb_per_g","drb_per_g","trb_per_g","ast_per_g","stl_per_g","blk_per_g","tov_per_g","pts_per_g"]
			for i in len(link_fields):
				stats[link_fields[i]] = year.xpath('th[@data-stat="' + link_fields[i] + '"]/a/text()').extract_first()
			for i in len(fields):
				stats[fields[i]] = year.xpath('td[@data-stat="' + fields[i] + '"]/text()').extract_first()
			yield stats

			'''
			stats["season"] = year.xpath('th[@data-stat="season"]/a/text()').extract_first()
			stats["age"] = year.xpath('td[@data-stat="age"]/text()').extract_first()
			stats["team"] = year.xpath('td[@data-stat="team_id"]/a/text()').extract_first()
			stats["league"] = year.xpath('td[@data-stat="lg_id"]/a/text()').extract_first()
			stats["position"] = year.xpath('td[@data-stat="pos"]/text()').extract_first()
			stats["games"] = year.xpath('td[@data-stat="g"]/text()').extract_first()
			stats["games_started"] = year.xpath('td[@data-stat="gs"]/text()').extract_first()
			stats["minutes_per_game"] = year.xpath('td[@data-stat="mp_per_g"]/text()').extract_first()
			stats["fg_per_game"] = year.xpath('td[@data-stat="fg_per_g"]/text()').extract_first()
			stats["fga_per_game"] = year.xpath('td[@data-stat="fga_per_g"]/text()').extract_first()
			stats["fg_pct"] = year.xpath('td[@data-stat="fg_pct"]/text()').extract_first()
			stats["fg3_per_game"] = year.xpath('td[@data-stat="fg3_per_g"]/text()').extract_first()
			stats["fg3a_per_game"] = year.xpath('td[@data-stat="fg3a_per_g"]/text()').extract_first()
			stats["fg3_pct"] = year.xpath('td[@data-stat="fg3_pct"]/text()').extract_first()
			stats["fg2_per_game"] = year.xpath('td[@data-stat="fg2_per_g"]/text()').extract_first()
			stats["fg2a_per_game"] = year.xpath('td[@data-stat="fg2a_per_g"]/text()').extract_first()
			stats["fg2_pct"] = year.xpath('td[@data-stat="fg2_pct"]/text()').extract_first()
			stats["efg_pct"] = year.xpath('td[@data-stat="efg_pct"]/text()').extract_first()
			stats["ft_per_game"] = year.xpath('td[@data-stat="ft_per_g"]/text()').extract_first()
			stats["fta_per_game"] = year.xpath('td[@data-stat="fta_per_g"]/text()').extract_first()
			stats["ft_pct"] = year.xpath('td[@data-stat="ft_pct"]/text()').extract_first()
			stats["orb_per_game"] = year.xpath('td[@data-stat="orb_per_g"]/text()').extract_first()
			stats["drb_per_game"] = year.xpath('td[@data-stat="drb_per_g"]/text()').extract_first()
			stats["trb_per_game"] = year.xpath('td[@data-stat="trb_per_g"]/text()').extract_first()
			stats["ast_per_game"] = year.xpath('td[@data-stat="ast_per_g"]/text()').extract_first()
			stats["stl_per_game"] = year.xpath('td[@data-stat="stl_per_g"]/text()').extract_first()
			stats["blk_per_game"] = year.xpath('td[@data-stat="blk_per_g"]/text()').extract_first()
			stats["tov_per_game"] = year.xpath('td[@data-stat="tov_per_g"]/text()').extract_first()
			stats["pts_per_game"] = year.xpath('td[@data-stat="pts_per_g"]/text()').extract_first()
			yield stats
			'''


		for total in totals:
			stats = Totals()
			stats["pid"] = player_id
			stats["name"] = name
			stats["season"] = total.xpath('th[@data-stat="season"]/a/text()').extract_first()
			stats["age"] = total.xpath('td[@data-stat="age"]/text()').extract_first()
			stats['team'] = total.xpath('td[@data-stat="team_id"]/a/text()').extract_first()
			stats["league"] = total.xpath('td[@data-stat="lg_id"]/a/text()').extract_first()
			stats["position"] = total.xpath('td[@data-stat="pos"]/text()').extract_first()
			stats["games"] = total.xpath('td[@data-stat="g"]/text()').extract_first()
			stats["games_started"] = total.xpath('td[@data-stat="gs"]/text()').extract_first()
			stats["minutes"] = total.xpath('td[@data-stat="mp"]/text()').extract_first()
			stats["fg"] = total.xpath('td[@data-stat="fg"]/text()').extract_first()
			stats["fga"] = total.xpath('td[@data-stat="fga"]/text()').extract_first()
			stats["fg_pct"] = total.xpath('td[@data-stat="fg_pct"]/text()').extract_first()
			stats["fg3"] = total.xpath('td[@data-stat="fg3"]/text()').extract_first()
			stats["fg3a"] = total.xpath('td[@data-stat="fg3a"]/text()').extract_first()
			stats["fg3_pct"] = total.xpath('td[@data-stat="fg3_pct"]/text()').extract_first()
			stats["fg2"] = total.xpath('td[@data-stat="fg2"]/text()').extract_first()
			stats["fg2a"] = total.xpath('td[@data-stat="fg2a"]/text()').extract_first()
			stats["fg2_pct"] = total.xpath('td[@data-stat="fg2_pct"]/text()').extract_first()
			stats["efg_pct"] = total.xpath('td[@data-stat="efg_pct"]/text()').extract_first()
			stats["ft"] = total.xpath('td[@data-stat="ft"]/text()').extract_first()
			stats["fta"] = total.xpath('td[@data-stat="fta"]/text()').extract_first()
			stats["ft_pct"] = total.xpath('td[@data-stat="ft_pct"]/text()').extract_first()
			stats["orb"] = total.xpath('td[@data-stat="orb"]/text()').extract_first()
			stats["drb"] = total.xpath('td[@data-stat="drb"]/text()').extract_first()
			stats["trb"] = total.xpath('td[@data-stat="trb"]/text()').extract_first()
			stats["ast"] = total.xpath('td[@data-stat="ast"]/text()').extract_first()
			stats["stl"] = total.xpath('td[@data-stat="stl"]/text()').extract_first()
			stats["blk"] = total.xpath('td[@data-stat="blk"]/text()').extract_first()
			stats["tov"] = total.xpath('td[@data-stat="tov"]/text()').extract_first()
			stats["pts"] = total.xpath('td[@data-stat="pts"]/text()').extract_first()
			yield stats

		for pos in per_pos:
			stats = PerPos()
			stats["pid"] = player_id
			stats["name"] = name
			stats["season"] = pos.xpath('th[@data-stat="season"]/a/text()').extract_first()
			stats["age"] = pos.xpath('td[@data-stat="age"]/text()').extract_first()
			stats['team'] = pos.xpath('td[@data-stat="team_id"]/a/text()').extract_first()
			stats["league"] = pos.xpath('td[@data-stat="lg_id"]/a/text()').extract_first()
			stats["position"] = pos.xpath('td[@data-stat="pos"]/text()').extract_first()
			stats["games"] = pos.xpath('td[@data-stat="g"]/text()').extract_first()
			stats["games_started"] = pos.xpath('td[@data-stat="gs"]/text()').extract_first()
			stats["minutes_per_pos"] = pos.xpath('td[@data-stat="mp"]/text()').extract_first()
			stats["fg_per_pos"] = pos.xpath('td[@data-stat="fg_per_poss"]/text()').extract_first()
			stats["fga_per_pos"] = pos.xpath('td[@data-stat="fga_per_poss"]/text()').extract_first()
			stats["fg_pct"] = pos.xpath('td[@data-stat="fg_pct"]/text()').extract_first()
			stats["fg3_per_pos"] = pos.xpath('td[@data-stat="fg3_per_poss"]/text()').extract_first()
			stats["fg3a_per_pos"] = pos.xpath('td[@data-stat="fg3a_per_poss"]/text()').extract_first()
			stats["fg3_pct"] = pos.xpath('td[@data-stat="fg3_pct"]/text()').extract_first()
			stats["fg2_per_pos"] = pos.xpath('td[@data-stat="fg2_per_poss"]/text()').extract_first()
			stats["fg2a_per_pos"] = pos.xpath('td[@data-stat="fg2a_per_poss"]/text()').extract_first()
			stats["fg2_pct"] = pos.xpath('td[@data-stat="fg2_pct"]/text()').extract_first()
			stats["ft_per_pos"] = pos.xpath('td[@data-stat="ft_per_poss"]/text()').extract_first()
			stats["fta_per_pos"] = pos.xpath('td[@data-stat="fta_per_poss"]/text()').extract_first()
			stats["ft_pct"] = pos.xpath('td[@data-stat="ft_pct"]/text()').extract_first()
			stats["orb_per_pos"] = pos.xpath('td[@data-stat="orb_per_poss"]/text()').extract_first()
			stats["drb_per_pos"] = pos.xpath('td[@data-stat="drb_per_poss"]/text()').extract_first()
			stats["trb_per_pos"] = pos.xpath('td[@data-stat="trb_per_poss"]/text()').extract_first()
			stats["ast_per_pos"] = pos.xpath('td[@data-stat="ast_per_poss"]/text()').extract_first()
			stats["stl_per_pos"] = pos.xpath('td[@data-stat="stl_per_poss"]/text()').extract_first()
			stats["blk_per_pos"] = pos.xpath('td[@data-stat="blk_per_poss"]/text()').extract_first()
			stats["tov_per_pos"] = pos.xpath('td[@data-stat="tov_per_poss"]/text()').extract_first()
			stats["pts_per_pos"] = pos.xpath('td[@data-stat="pts_per_poss"]/text()').extract_first()
			stats["off_rtg"] = pos.xpath('td[@data-stat="off_rtg"]/text()').extract_first()
			stats["def_rtg"] = pos.xpath('td[@data-stat="def_rtg"]/text()').extract_first()
			yield stats

