from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from playerByGame import yearGameStats
from bs4 import Comment

#my_url = 'https://www.basketball-reference.com/players/d/duranke01.html'

def playerStats(link,seasonfile,gamesfile):
	# opening up connection grabbing the page
	uClient = uReq(link)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grabs each product
	stats = page_soup.find("div",{"id":"content"})
	statsByYear = stats.div.findAll("tr",{"class":"full_table"})

	#filename = "DurantStats.csv"
	#f = open(filename,"w")
	#headers = "SEASON,AGE,TEAM,POS,G,GS,MIN,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,EFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS\n"
	#f.write(headers)

	#gamesfilename = "DurantGameStats.csv"
	#gamesfile = open(gamesfilename,"w")
	#gamesheaders = "TEAMGAME,GAMEPLAYED,DATE,AGE,TEAM,HOME/AWAY,OPP,WIN/LOSS,MARGIN,START,MIN,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GAMESCORE,+/-\n"
	#gamesfile.write(gamesheaders)


	for yearStats in statsByYear:

		link = 'https://www.basketball-reference.com' + yearStats.th.find('a',href=True)['href']

		season = yearStats.a.text
		age = yearStats.find("td",{"data-stat":"age"}).text
		team = yearStats.find("td",{"data-stat":"team_id"}).text
		pos = yearStats.find("td",{"data-stat":"pos"}).text
		games = yearStats.find("td",{"data-stat":"g"}).text
		gamesStarted = yearStats.find("td",{"data-stat":"gs"}).text
		minutes = yearStats.find("td",{"data-stat":"mp_per_g"}).text
		fg = yearStats.find("td",{"data-stat":"fg_per_g"}).text
		fga = yearStats.find("td",{"data-stat":"fga_per_g"}).text
		fgpct = yearStats.find("td",{"data-stat":"fg_pct"}).text
		fg3 = yearStats.find("td",{"data-stat":"fg3_per_g"}).text
		fg3a = yearStats.find("td",{"data-stat":"fg3a_per_g"}).text
		fg3pct = yearStats.find("td",{"data-stat":"fg3_pct"}).text
		fg2 = yearStats.find("td",{"data-stat":"fg2_per_g"}).text
		fg2a = yearStats.find("td",{"data-stat":"fg2a_per_g"}).text
		fg2pct = yearStats.find("td",{"data-stat":"fg2_pct"}).text
		efgpct = yearStats.find("td",{"data-stat":"efg_pct"}).text
		ft = yearStats.find("td",{"data-stat":"ft_per_g"}).text
		fta = yearStats.find("td",{"data-stat":"fta_per_g"}).text
		ftpct = yearStats.find("td",{"data-stat":"ft_pct"}).text
		orb = yearStats.find("td",{"data-stat":"orb_per_g"}).text
		drb = yearStats.find("td",{"data-stat":"drb_per_g"}).text
		trb = yearStats.find("td",{"data-stat":"trb_per_g"}).text
		ast =  yearStats.find("td",{"data-stat":"ast_per_g"}).text
		stl =  yearStats.find("td",{"data-stat":"stl_per_g"}).text
		blk = yearStats.find("td",{"data-stat":"blk_per_g"}).text
		tov = yearStats.find("td",{"data-stat":"tov_per_g"}).text
		pf = yearStats.find("td",{"data-stat":"pf_per_g"}).text
		pts = yearStats.find("td",{"data-stat":"pts_per_g"}).text

		seasonfile.write(season + "," +
			age + "," +
			team + "," +
			pos + "," +
			games + "," +
			gamesStarted + "," +
			minutes + "," +
			fg + "," +
			fga + "," +
			fgpct + "," +
			fg3 + "," +
			fg3a + "," +
			fg3pct + "," +
			fg2 + "," +
			fg2a + "," +
			fg2pct + "," +
			efgpct + "," +
			ft + "," +
			fta + "," +
			ftpct + "," +
			orb + "," +
			drb + "," +
			trb + "," +
			ast + "," +
			stl + "," +
			blk + "," +
			tov + "," +
			pf + "," +
			pts + "\n")

		yearGameStats(link,gamesfile)