from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

def yearGameStats(link,file):
	# opening up connection grabbing the page

	print(link)
	
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grabs each product
	stats = page_soup.find("div",{"id":"content"})
	statsByGame = stats.findAll("div")[15]
	statsByGame = statsByGame.find("div",{"class":"overthrow table_container"})
	statsByGame = statsByGame.find("tbody").findAll("tr")

	for gameStats in statsByGame:

		teamGame = gameStats.find("th",{"data-stat":"ranker"}).text
		if(teamGame == "Rk"):
			continue
		if gameStats.find("td",{"data-stat":"gs"}) is None:
			continue
		gamePlayed = gameStats.find("td",{"data-stat":"game_season"}).text
		date = gameStats.find("td",{"data-stat":"date_game"}).text
		age = gameStats.find("td",{"data-stat":"age"}).text
		team = gameStats.find("td",{"data-stat":"team_id"}).text
		homeAway = gameStats.find("td",{"data-stat":"game_location"}).text
		opp = gameStats.find("td",{"data-stat":"opp_id"}).text
		
		gameResult = gameStats.find("td",{"data-stat":"game_result"}).text
		listResult = list(filter(None,re.split(r'[()\s]\s*',gameResult)))

		#split game game_result
		winLoss = listResult[0]
		margin = listResult[1]

		start = gameStats.find("td",{"data-stat":"gs"}).text

		mins = gameStats.find("td",{"data-stat":"mp"}).text
		fg = gameStats.find("td",{"data-stat":"fg"}).text
		fga = gameStats.find("td",{"data-stat":"fga"}).text
		fg_pct = gameStats.find("td",{"data-stat":"fg_pct"}).text
		fg3 = gameStats.find("td",{"data-stat":"fg3"}).text
		fg3a = gameStats.find("td",{"data-stat":"fg3a"}).text
		fg3_pct = gameStats.find("td",{"data-stat":"fg3_pct"}).text
		ft = gameStats.find("td",{"data-stat":"ft"}).text
		fta = gameStats.find("td",{"data-stat":"fta"}).text
		ft_pct = gameStats.find("td",{"data-stat":"ft_pct"}).text
		orb = gameStats.find("td",{"data-stat":"orb"}).text
		drb = gameStats.find("td",{"data-stat":"drb"}).text
		trb = gameStats.find("td",{"data-stat":"trb"}).text
		ast = gameStats.find("td",{"data-stat":"ast"}).text
		stl = gameStats.find("td",{"data-stat":"stl"}).text
		blk = gameStats.find("td",{"data-stat":"blk"}).text
		tov = gameStats.find("td",{"data-stat":"tov"}).text
		pf = gameStats.find("td",{"data-stat":"pf"}).text
		pts = gameStats.find("td",{"data-stat":"pts"}).text
		gameScore = gameStats.find("td",{"data-stat":"game_score"}).text
		plus_minus = gameStats.find("td",{"data-stat":"plus_minus"}).text


		file.write(teamGame + "," +
			gamePlayed + "," +
			date + "," +
			age + "," +
			team + "," +
			homeAway + "," +
			opp + "," +
			winLoss + "," +
			margin + "," +
			start + "," +
			mins + "," +
			fg + "," +
			fga + "," +
			fg_pct + "," +
			fg3 + "," +
			fg3a + "," +
			fg3_pct + "," +
			ft + "," +
			fta + "," +
			ft_pct + "," +
			orb + "," +
			drb + "," +
			trb + "," +
			ast + "," +
			stl + "," +
			blk + "," +
			tov + "," +
			pf + "," +
			pts + "," +
			gameScore + "," +
			plus_minus + "\n")