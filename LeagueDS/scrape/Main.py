import csv
import json
import random
import time
from RiotAPI import RiotAPI
from ChampionGGAPI import ChampionAPI

def main():
    api_key='RGAPI-f2907155-7488-4446-9b9c-ef8332e10674'
    #collect_champions(api_key)
    scrape_match_data(api_key)

def collect_champions(api_key):
    csvfile = 'champions_data.csv'
    output = open(csvfile,'a')
    api = RiotAPI(api_key)
    r = api.get_champion_list()
    while r is None or r.get('data') is None    :
        r = api.get_champion_list()

    print(r.get('data'))
    for champion in r.get('data'):
        temp = r.get('data')[champion]
        c = [temp.get('name'),temp.get('id')]
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(c)
    output.close()


def scrape_match_data(api_key):
    csvfile = 'match_data2.csv'
    matches = []
    searched_matches = []
    accounts = []
    searched_accounts = []
    count = 0

    accounts.append('32639237')

    api = RiotAPI(api_key)

    while accounts:
        nextAccount = accounts.pop()
        r = api.get_matchlist(nextAccount)
        while r is None or r.get('matches') is None:
            time.sleep(3)
            #nextAccount = accounts.pop()
            r = api.get_matchlist(nextAccount)

        searched_accounts.append(nextAccount)

        for match in r.get('matches'):
            if match.get('platformId')=='NA1':
                Id = match.get('gameId')
                if Id not in searched_matches:
                    matches.append(Id)
        random.shuffle(matches)

        output = open(csvfile, 'a')
        while matches:
            nextMatch = matches.pop()
            searched_matches.append(nextMatch)
            count+=1
            print(count)

            r = api.get_match(nextMatch)
            while r is None or r.get('participantIdentities') is None:
                time.sleep(3)
                r = api.get_match(nextMatch)

            for player in r.get('participantIdentities'):
                accountId = player.get('player').get('currentAccountId')
                if accountId not in searched_accounts:
                    accounts.append(accountId)
            random.shuffle(accounts)

            winning_champions = []
            losing_champions = []
            for player in r.get('participants'):
                win = player.get('stats').get('win')
                champion = player.get('championId')

                if win == True:
                    winning_champions.append(champion)
                else:
                    losing_champions.append(champion)
            game = []
            for winners in winning_champions:
                game.append(winners)
            for losers in losing_champions:
                game.append(losers)

            print(game)

            writer = csv.writer(output,lineterminator='\n')
            writer.writerow(game)
        output.close()


    #api2 = ChampionAPI('a2e5ce856256b8ec6013875215c78006')
    #p = api2.get_all_champions()
    #p = api2.get_champion(id='1')
    #p = api2.get_champion_matchup(id='1')


if __name__ == "__main__":
    main()
