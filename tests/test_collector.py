from __future__ import annotations

from riot_api.collector import RiotMatchCollector


class FakeClient:
    def __init__(self):
        self.urls = []

    def get_json(self, url, params=None):
        self.urls.append(url)
        if "/entries/by-puuid/" in url:
            return [{"queueType": "RANKED_SOLO_5x5", "tier": "GOLD", "rank": "I"}]
        if "/champion-masteries/" in url:
            return {"championLevel": 7}
        raise AssertionError(url)


def test_rank_lookup_is_cached_by_puuid():
    client = FakeClient()
    collector = RiotMatchCollector(client)
    errors = []
    assert collector.get_solo_rank("p1", errors)["tier"] == "GOLD"
    assert collector.get_solo_rank("p1", errors)["tier"] == "GOLD"
    assert len([url for url in client.urls if "/entries/by-puuid/" in url]) == 1


def test_mastery_lookup_is_cached_by_puuid_and_champion():
    client = FakeClient()
    collector = RiotMatchCollector(client)
    errors = []
    assert collector.get_mastery("p1", 103, errors)["championLevel"] == 7
    assert collector.get_mastery("p1", 103, errors)["championLevel"] == 7
    assert len([url for url in client.urls if "/champion-masteries/" in url]) == 1


class MatchClient:
    def __init__(self):
        self.urls = []

    def get_json(self, url, params=None):
        self.urls.append(url)
        return {"url": url}


def test_match_and_timeline_are_cached_by_match_id():
    client = MatchClient()
    collector = RiotMatchCollector(client)
    collector.get_match("KR_1")
    collector.get_match("KR_1")
    collector.get_timeline("KR_1")
    collector.get_timeline("KR_1")
    assert len(client.urls) == 2
    assert client.urls[0].endswith("/matches/KR_1")
    assert client.urls[1].endswith("/matches/KR_1/timeline")
