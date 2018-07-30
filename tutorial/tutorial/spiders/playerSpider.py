import scrapy
from scrapy_splash import SplashRequest
from scrapy.item import Item
from scrapy.item import Field
from .MyItems import PerGame, Totals, PerPos, Advanced, Shooting, Play_By_Play, Playoffs_PerGame, Playoffs_Totals, Playoffs_PerPos, Playoffs_Advanced, Playoffs_Shooting, Playoffs_Play_By_Play

player_id = 0

#if none, look for strong font

def getText(source,field):
	if(source.xpath('td[@data-stat="' + field + '"]/text()').extract_first() == None):
		return source.xpath('td[@data-stat="' + field + '"]/strong/text()').extract_first()
	else:
		return source.xpath('td[@data-stat="' + field + '"]/text()').extract_first()

def fillStats(source,item,name,link_fields,fields):
	global player_id
	item["pid"] = player_id
	item["name"] = name
	item["season"] = source.xpath('th[@data-stat="season"]/a/text()').extract_first()
	for i in range(0,len(link_fields)):
		item[link_fields[i]] = source.xpath('td[@data-stat="' + link_fields[i] + '"]/a/text()').extract_first()
	for i in range(0,len(fields)):
		item[fields[i]] = getText(source,fields[i])
	return item

def addHyphens(source,item,hyphen_fields):
	for i in range(0,len(hyphen_fields)):
		print(hyphen_fields[i])
		item[hyphen_fields[i].replace("-","_")] = source.xpath('td[@data-stat="' + hyphen_fields[i].replace("_","-") + '"]/text()').extract_first()
		print(hyphen_fields[i])
	return item

class PlayerSpider(scrapy.Spider):
	name = "playerSpider"

	start_urls = ["https://www.basketball-reference.com/players/d/duranke01.html"]

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

	def parse(self, response):
		name = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()
		per_game = response.selector.xpath('//table[@id="per_game"]/tbody/tr[@class="full_table"]')
		totals = response.selector.xpath('//table[@id="totals"]/tbody/tr[@class="full_table"]')
		per_pos = response.selector.xpath('//table[@id="per_poss"]/tbody/tr[@class="full_table"]')
		advanced = response.selector.xpath('//table[@id="advanced"]/tbody/tr[@class="full_table"]')
		shooting = response.selector.xpath('//table[@id="shooting"]/tbody/tr[@class="full_table"]')
		play_by_play = response.selector.xpath('//table[@id="advanced_pbp"]/tbody/tr[@class="full_table"]')
		playoffs = response.selector.xpath('//table[@id="playoffs_per_game"]/tbody/tr[@class="full_table"]')
		playoffs_totals = response.selector.xpath('//table[@id="playoffs_totals"]/tbody/tr[@class="full_table"]')
		playoffs_per_poss = response.selector.xpath('//table[@id="playoffs_per_poss"]/tbody/tr[@class="full_table"]')
		playoffs_advanced = response.selector.xpath('//table[@id="playoffs_advanced"]/tbody/tr[@class="full_table"]')
		playoffs_shooting = response.selector.xpath('//table[@id="playoffs_shooting"]/tbody/tr[@class="full_table"]')
		playoffs_play_by_play = response.selector.xpath('//table[@id="playoffs_advanced_pbp"]/tbody/tr[@class="full_table"]')

		for year in per_game:
			stats = PerGame()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp_per_g","fg_per_g","fga_per_g","fg_pct","fg3_per_g",
				"fg3a_per_g","fg3_pct","fg2_per_g","fg2a_per_g","fg2_pct","efg_pct","ft_per_g",
				"fta_per_g","ft_pct","orb_per_g","drb_per_g","trb_per_g","ast_per_g","stl_per_g",
				"blk_per_g","tov_per_g","pf_per_g","pts_per_g"]
			yield fillStats(year,stats,name,link_fields,fields)

		for total in totals:
			stats = Totals()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp","fg","fga","fg_pct","fg3","fg3a","fg3_pct","fg2",
				"fg2a","fg2_pct","efg_pct","ft","fta","ft_pct","orb","drb","trb","ast","stl","blk",
				"tov","pf","pts"]
			yield fillStats(total,stats,name,link_fields,fields)

		for pos in per_pos:
			stats = PerPos()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp","fg_per_poss","fga_per_poss","fg_pct","fg3_per_poss",
				"fg3a_per_poss","fg3_pct","fg2_per_poss","fg2a_per_poss","fg2_pct","ft_per_poss",
				"fta_per_poss","ft_pct","orb_per_poss","drb_per_poss","trb_per_poss","ast_per_poss",
				"stl_per_poss","blk_per_poss","tov_per_poss","pf_per_poss","pts_per_poss","off_rtg",
				"def_rtg"]
			yield fillStats(pos,stats,name,link_fields,fields)

		for adv in advanced:
			stats = Advanced()
			link_fields = ["team_id","lg_id"]
			hyphen_fields = ["ws-dum","bpm-dum"]
			fields = ["age","pos","g","mp","per","ts_pct","fg3a_per_fga_pct","fta_per_fga_pct",
				"orb_pct","drb_pct","trb_pct","ast_pct","stl_pct","blk_pct","tov_pct","usg_pct",
				"ows","dws","ws","ws_per_48","obpm","dbpm","bpm","vorp"]
			stats = fillStats(adv,stats,name,link_fields,fields)
			yield addHyphens(adv,stats,hyphen_fields)

		for shoot in shooting:
			stats = Shooting()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","mp","fg_pct","avg_dist","fg2a_pct_fga","pct_fga_00_03",
				"pct_fga_03_10","pct_fga_10_16","pct_fga_16_xx","fg3a_pct_fga","fg2_pct",
				"fg_pct_00_03","fg_pct_03_10","fg_pct_10_16","fg_pct_16_xx","fg3_pct","fg2_pct_ast",
				"pct_fg2_dunk","fg2_dunk","fg3_pct_ast","pct_fg3a_corner","fg3_pct_corner",
				"fg3a_heave","fg3_heave"]
			yield fillStats(shoot,stats,name,link_fields,fields)

		for play in play_by_play:
			stats = Play_By_Play()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","mp","pct_1","pct_2","pct_3","pct_4","pct_5","plus_minus_on",
				"plus_minus_net","tov_bad_pass","tov_lost_ball","tov_other","fouls_shooting",
				"fouls_blocking","fouls_offensive","fouls_take","astd_pts","drawn_shooting",
				"and1s","fga_blkd"]
			yield fillStats(play,stats,name,link_fields,fields)

		for playoff in playoffs:
			stats = Playoffs_PerGame()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp_per_g","fg_per_g","fga_per_g","fg_pct","fg3_per_g",
				"fg3a_per_g","fg3_pct","fg2_per_g","fg2a_per_g","fg2_pct","efg_pct","ft_per_g",
				"fta_per_g","ft_pct","orb_per_g","drb_per_g","trb_per_g","ast_per_g","stl_per_g",
				"blk_per_g","tov_per_g","pf_per_g","pts_per_g"]
			yield fillStats(playoff,stats,name,link_fields,fields)

		for playoff_total in playoffs_totals:
			stats = Playoffs_Totals()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp","fg","fga","fg_pct","fg3","fg3a","fg3_pct","fg2",
				"fg2a","fg2_pct","efg_pct","ft","fta","ft_pct","orb","drb","trb","ast","stl","blk",
				"tov","pf","pts"]
			yield fillStats(playoff_total,stats,name,link_fields,fields)

		for playoff_pos in playoffs_per_poss:
			stats = Playoffs_PerPos()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","gs","mp","fg_per_poss","fga_per_poss","fg_pct","fg3_per_poss",
				"fg3a_per_poss","fg3_pct","fg2_per_poss","fg2a_per_poss","fg2_pct","ft_per_poss",
				"fta_per_poss","ft_pct","orb_per_poss","drb_per_poss","trb_per_poss","ast_per_poss",
				"stl_per_poss","blk_per_poss","tov_per_poss","pf_per_poss","pts_per_poss","off_rtg",
				"def_rtg"]
			yield fillStats(playoff_pos,stats,name,link_fields,fields)

		for playoff_adv in playoffs_advanced:
			stats = Playoffs_Advanced()
			link_fields = ["team_id","lg_id"]
			hyphen_fields = ["ws_dum","bpm_dum"]
			fields = ["age","pos","g","mp","per","ts_pct","fg3a_per_fga_pct","fta_per_fga_pct",
				"orb_pct","drb_pct","trb_pct","ast_pct","stl_pct","blk_pct","tov_pct","usg_pct",
				"ows","dws","ws","ws_per_48","obpm","dbpm","bpm","vorp"]
			stats = fillStats(playoff_adv,stats,name,link_fields,fields)
			yield addHyphens(playoff_adv,stats,hyphen_fields)

		for playoff_shoot in playoffs_shooting:
			stats = Playoffs_Shooting()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","mp","fg_pct","avg_dist","fg2a_pct_fga","pct_fga_00_03",
				"pct_fga_03_10","pct_fga_10_16","pct_fga_16_xx","fg3a_pct_fga","fg2_pct",
				"fg_pct_00_03","fg_pct_03_10","fg_pct_10_16","fg_pct_16_xx","fg3_pct","fg2_pct_ast",
				"pct_fg2_dunk","fg2_dunk","fg3_pct_ast","pct_fg3a_corner","fg3_pct_corner",
				"fg3a_heave","fg3_heave"]
			yield fillStats(playoff_shoot,stats,name,link_fields,fields)

		for playoff_play in playoffs_play_by_play:
			stats = Playoffs_Play_By_Play()
			link_fields = ["team_id","lg_id"]
			fields = ["age","pos","g","mp","pct_1","pct_2","pct_3","pct_4","pct_5","plus_minus_on",
				"plus_minus_net","tov_bad_pass","tov_lost_ball","tov_other","fouls_shooting",
				"fouls_blocking","fouls_offensive","fouls_take","astd_pts","drawn_shooting",
				"and1s","fga_blkd"]
			yield fillStats(playoff_play,stats,name,link_fields,fields)





