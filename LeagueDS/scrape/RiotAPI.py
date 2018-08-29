from ratelimit import rate_limited
import time
import requests
import RiotConsts as Consts

class RiotAPI(object):
    def __init__(self, api_key, region=Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        self.time = time.time()

    @rate_limited(5,6)
    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        now = time.time()
        print(now - self.time)

        response = requests.get(
            Consts.URL['base'].format(
                region=self.region,
                url=api_url
            ),
            params=args
        )

        self.time=now

        print(response.url)
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_champion_list(self):
        api_url = Consts.URL['champion_list'].format(
            version=Consts.API_VERSIONS['summoner']
        )
        return self._request(api_url)

    def get_matchlist(self, accountID):
        api_url = Consts.URL['matchlist'].format(
            accountId=accountID
        )
        return self._request(api_url)

    def get_match(self, matchId):
        api_url = Consts.URL['match'].format(
            matchId=matchId
        )
        return self._request(api_url)

