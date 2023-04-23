import requests

from bs4 import BeautifulSoup
import urllib.parse
from typing import Optional, Mapping, Literal


class SnookerOrg(object):
    BASE_URL: str = "https://api.snooker.org/"
    SEASON_EVENTS_T: int = 5
    EVENT_MATCHES_T: int = 6
    ONGOING_MATCHES_T: int = 7
    PLAYER_SEASON_MATCHES_T: int = 8
    EVENT_PLAYERS_T: int = 9
    SEASON_PLAYERS_T: int = 10
    ROUND_INFO_T: int = 12
    EVENT_SEEDING_T: int = 13
    MATCHES_UPCOMING_T: int = 14
    EVENT: str = "e"
    PLAYER: str = "p"
    ROUND: str = "r"
    MATCH: str = "n"
    SEASON: str = "s"
    PRO: str = "p"
    AMATEUR: str = "a"
    TYPE: str = "t"
    RANKING: str = "rt"

    def __init__(self) -> None:
        return None

    def _requests_url(self, params: Mapping[str, str | int]) -> str:
        return f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"

    def _extract_json(self, r: requests.models.Response) -> Mapping[str, str]:
        if len(r.json()) == 1:
            return r.json()[0]
        else:
            return {str(key): r.json()[key] for key in range(len(r.json()))}

    def _get(self, params: Mapping[str, str | int]) -> Mapping[str, str]:
        r: requests.Response = requests.get(self._requests_url(params))
        return self._extract_json(r)

    def get_info_dic(self) -> BeautifulSoup:
        r: requests.Response = requests.get(self.BASE_URL)
        info: BeautifulSoup = BeautifulSoup(r.text)
        return info

    def get_event_dic(self, event_id: int) -> Mapping[str, str]:
        params: dict[str, int] = {self.EVENT: event_id}
        return self._get(params)

    def get_match_dic(
        self, event_id: int, round_id: int, match_nbr: int
    ) -> Mapping[str, str]:
        params: dict[str, int] = {
            self.EVENT: event_id,
            self.ROUND: round_id,
            self.MATCH: match_nbr,
        }
        return self._get(params)

    def get_player_dic(self, player_id: int) -> Mapping[str, str]:
        params: dict[str, int] = {self.PLAYER: player_id}
        return self._get(params)

    def get_events_dic(self, season_year: int) -> Mapping[str, str]:
        params: dict[str, int] = {
            self.TYPE: self.SEASON_EVENTS_T,
            self.SEASON: season_year,
        }
        return self._get(params)

    def get_event_matches_dic(self, event_id: int) -> Mapping[str, str]:
        params: dict[str, int] = {self.TYPE: self.EVENT_MATCHES_T, self.EVENT: event_id}
        return self._get(params)

    def get_ongoing_dic(self) -> Mapping[str, str]:
        params: dict[str, int] = {self.TYPE: self.ONGOING_MATCHES_T}
        return self._get(params)

    def get_player_matches_dic(
        self, player_id: int, season_year: int
    ) -> Mapping[str, str]:
        params: dict[str, int] = {
            self.TYPE: self.PLAYER_SEASON_MATCHES_T,
            self.PLAYER: player_id,
            self.SEASON: season_year,
        }
        return self._get(params)

    def get_event_players_dic(self, event_id: int) -> Mapping[str, str]:
        params: dict[str, int] = {self.TYPE: self.EVENT_PLAYERS_T, self.EVENT: event_id}
        return self._get(params)

    def get_players_dic(
        self, season_year: int, pros: Optional[bool] = True
    ) -> Mapping[str, str]:
        p: Literal["p", "a"] = "p" if pros else "a"
        params: dict[str, str | int] = {
            self.TYPE: self.SEASON_PLAYERS_T,
            self.PLAYER: p,
            self.SEASON: season_year,
        }
        return self._get(params)

    def get_rankings_dic(self, ranking_type: str) -> Mapping[str, str]:
        # MoneyRankings (2013-), MoneySeedings (2013-), OneYearMoneyRankings (2013-), QTRankings (2021-), WomensRankings (2022-), ProjectedMoneyRankings (2013-), ProjectedMoneySeedings (2013-), ProvOneYearMoneyRankings (2013-), ProjectedEndOfSeasonMoneySeedings (2014-), ProjectedGrandPrixMoneyRankings (2014-), ProjectedPCMoneyRankings (2016-), ProjectedWCMoneySeedings (2017-), ProjectedQTRankings (2021-)
        """
        Args:
            ranking_type (str): Available ranking types: MoneyRankings (2013-), MoneySeedings (2013-), OneYearMoneyRankings (2013-), QTRankings (2021-), WomensRankings (2022-), ProjectedMoneyRankings (2013-), ProjectedMoneySeedings (2013-), ProvOneYearMoneyRankings (2013-), ProjectedEndOfSeasonMoneySeedings (2014-), ProjectedGrandPrixMoneyRankings (2014-), ProjectedPCMoneyRankings (2016-), ProjectedWCMoneySeedings (2017-), ProjectedQTRankings (2021-)
        Returns:
            Mapping[str, str]: description
        """
        params: dict[str, str] = {self.RANKING: ranking_type}
        return self._get(params)

    def get_round_info_dic(
        self, event_id: Optional[int] = None, season_year: Optional[int] = None
    ) -> Mapping[str, str]:
        params: dict[str, int] = {self.TYPE: self.ROUND_INFO_T}
        if event_id:
            params.update({self.EVENT: event_id})
        if season_year:
            params.update({self.SEASON: season_year})
        return self._get(params)

    def get_seeds_dic(self, event_ind: int) -> Mapping[str, str]:
        params: dict[str, int] = {
            self.TYPE: self.EVENT_SEEDING_T,
            self.EVENT: event_ind,
        }
        return self._get(params)

    def get_upcoming_dic(self) -> Mapping[str, str]:
        params: dict[str, int] = {self.TYPE: self.MATCHES_UPCOMING_T}
        return self._get(params)
