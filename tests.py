import unittest

from httmock import urlmatch, HTTMock

import lineup
import standings


class TestLineup(unittest.TestCase):
    @urlmatch(netloc=r'http\:\/\/games\.espn\.go\.com\/ffl\/clubhouse\?.')
    def lineup_mock(url, request):
        return open('test_data/team.html').read()

    def test_lineup(self):
        url = ('http://games.espn.go.com/ffl/clubhouse?leagueId=844419'
               '&teamId=8&seasonId=2013')
        with HTTMock(self.lineup_mock):
            players = lineup.scrape(url)
        self.assertEqual(21, len(players))


class TestStandings(unittest.TestCase):
    @urlmatch(netloc=r'http\:\/\/games\.espn\.go\.com\/ffl\/standings\?.')
    def standings_mock(url, request):
        return open('test_data/standings.html').read()

    def test_standings(self):
        url = ('http://games.espn.go.com/ffl/standings?leagueId=844419'
               '&seasonId=2013')
        with HTTMock(self.standings_mock):
            teams = standings.scrape(url)
        self.assertEqual(8, len(teams))


# class TestScoreboard(unittest.TestCase):
# @urlmatch(netloc=r'http\:\/\/games\.espn\.go\.com\/ffl\/scoringPeriodId\?.')
#     def scoreboard_mock(url, request):
#         return open('test_data/scoreboard.html').read()
#
#     def test_scoreboard(self):
#         url = ('http://games.espn.go.com/ffl/scoreboard?leagueId=844419'
#                '&scoringPeriodId=17')
#         # with HTTMock(self.scoreboard_mock):
#         scores = scoreboard.scrape(url)
#         self.assertEqual(8, len(scores))

if __name__ == '__main__':
    unittest.main()
