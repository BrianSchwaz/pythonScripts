from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from playerScrape import playerStats
from playerByGame import findData
from urllib.error import HTTPError
from urllib.error import URLError

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
foundPlayer = True #set false if looking for specific stat
searchingPlayer = "Neil Johnston*"
playerID = 1

def main():
	errors = 0
	try:
		my_url = 'https://www.basketball-reference.com/players/'
		
		# opening up connection grabbing the page
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#html parsing
		page_soup = soup(page_html, "html.parser")

		#grabs each product
		mainHtml = page_soup.find("div",{"id":"content"})
		alphabet = mainHtml.find("ul").findAll('li')

		playerGeneral = "PlayerGeneral.csv"
		player_general = open(playerGeneral,"a")#changed to a for appending
		player_general.write("ID,NAME,STARTYEAR,ENDYEAR,POS,HT,WT,BIRTHDATE,COLLEGE,HALLOF_fame\n")
		#player_general.write(generalheaders)

		PlayerSeasonAvg = "PlayerSeasonAvg.csv"
		player_season_avg = open(player_season_avg,"a")#changed to a for appending
		player_season_avg.write("ID,NAME,SEASON,AGE,TEAM,POS,G,GS,MIN,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,EFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS\n")
		#player_stats.write(playerheaders)

		PlayerSeasonTotals = "PlayerSeasonTotals.csv"
		player_season_totals = open(player_season_totals,"a")#changed to a for appending
		player_season_totals.write("ID,NAME,SEASON,AGE,TEAM,POS,G,GS,MIN,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,EFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS\n")
		#player_stats.write(playerheaders)

		playerSeasonGames= "PlayerSeasonGames.csv"
		player_season_games = open(player_season_games,"a")#changed to a for appending
		player_season_games.write("ID,NAME,TEAMGAME,GAMEPLAYED,DATE,AGE,TEAM,HOME/AWAY,OPP,WIN/LOSS,MARGIN,START,MIN,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GAMESCORE,+/-\n")
		#gamesfile.write(gamesheaders)
		


		for letter in alphabet:

			letterlink = letter.find('a',href=True)
			if(letterlink == None):
				continue
			link = 'https://www.basketball-reference.com' + letterlink['href']
			goToLetter(link,player_general,player_stats,gamesfile,errors)

		gamesfile.close()
		player_stats.close()
		player_general.close()
		print(playerID)

	except (HTTPError, URLError) as error:
		print("INITIAL CONNECTION ERROR")

	"""
	print("\nFINISHED\n")
	print(playerGeneralString)
	print(playerStatsString)
	print(playerGamesString)
	print("\nEND FINISHED\n")
	"""



def goToLetter(link,player_general,player_stats,gamesfile,errors):
	global foundPlayer
	global playerID
	try:
		letterClient = uReq(link)
		letter_html = letterClient.read()
		letterClient.close()

		#html parsing
		lettersoup = soup(letter_html, "html.parser")

		mainLetter = lettersoup.find("div",{"id":"all_players"})
		players = mainLetter.tbody.findAll("tr")

		for player in players:

			playerNameLink = player.th.find('a',href=True)
			if(playerNameLink == None):
				continue
			playerlink = 'https://www.basketball-reference.com' + playerNameLink['href']

			pID = playerID
			playerID += 1
			name = player.find("th",{"data-stat":"player"}).text
			if(foundPlayer == False):
				if(name != searchingPlayer):
					continue
				else:
					foundPlayer = True
			if ("*" in name):
				hall_of_fame = True
				name = name.replace("*","")
			print(name)
			
			start = player.find("td",{"data-stat":"year_min"}).text
			end = player.find("td",{"data-stat":"year_max"}).text
			pos = player.find("td",{"data-stat":"pos"}).text
			height = player.find("td",{"data-stat":"height"}).text
			weight = player.find("td",{"data-stat":"weight"}).text
			birth = player.find("td",{"data-stat":"birth_date"}).text
			college = player.find("td",{"data-stat":"colleges"}).text

			player_general.write(str(str(pID) + "," +
				name + "," +
				start + "," +
				end + "," +
				pos + "," +
				height + "," +
				weight + "," +
				birth + "," +
				college + "\n"))

			playerStats(playerlink,player_stats,gamesfile,pID,name,errors)

		#print("\nGENERAL:\n" + playerGeneralString + "\nGENERAL END\n")

	except (HTTPError, URLError) as error:
		print("LETTER CONNECTION ERROR")
		errors += 1
		if(errors < 100):
			print(errors)
			goToLetter(link,player_stats,gamesfile,playerID,errors)
		else:
			exit()
	except KeyboardInterrupt:
		print("Someone closed the program\n")
		exit()


if __name__ == "__main__":
	main()