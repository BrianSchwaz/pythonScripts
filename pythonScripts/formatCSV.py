import csv
import pandas


def main():

	data = pandas.read_csv("PlayerGameStats.csv")
	data = data.drop(['ID'])
	data.to_csv("FormattedGameStats.csv")

"""
	with open("PlayerGameStats.csv","rb") as player_game_stats:
		reader = csv.reader(player_game_stats)
		with open ("FormattedGameStats.csv","wb") as result:
			writer = csv.writer(result)
			for r in reader:
				writer.writerow()
"""


if __name__ == "__main__":
	main()