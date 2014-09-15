import unittest

import httmock

import lineup
import standings
import team


class TestLineup(unittest.TestCase):
    @httmock.all_requests
    def lineup_mock(self, url, request):
        return open('test_data/lineup.html').read()

    def test_lineup(self):
        expected_player = {
            'slot': u'QB',
            'name': u'Nick Foles',
            'ownership_change': u'+0',
            'average': u'17.7',
            'last_points': u'17.4',
            'player_rank': u'13',
            'opponent_rank': u'--',
            'projected_points': u'--',
            'team': u'Phi',
            'position': u'QB',
            'percent_starting': u'67.2',
            'percent_own': u'88.4',
            'points': u'282.6'}
        with httmock.HTTMock(self.lineup_mock):
            players = lineup.scrape(1, 1, 2014)
        self.assertEqual(21, len(players))
        self.assertEqual(expected_player, players[0])


class TestStandings(unittest.TestCase):
    @httmock.all_requests
    def standings_mock(self, url, request):
        return open('test_data/standings.html').read()

    def test_standings(self):
        expected_team = {'streak': u'W4',
                         'games_behind': u'--',
                         'name': 'Hoyer The Destroyed',
                         'points_against': u'1382',
                         'wins': u'11',
                         'losses': u'3',
                         'division_record': u'11-3-0',
                         'home_record': u'6-1-0',
                         'points_for': u'1744.1',
                         'away_record': u'5-2-0',
                         'owner': 'Josh Gachnang)',
                         'ties': u'0',
                         'percentage': u'.786'}

        with httmock.HTTMock(self.standings_mock):
            teams = standings.scrape(1, 2014)
        self.assertEqual(8, len(teams))
        self.assertEqual(expected_team, teams[0])


class TestScoreboard(unittest.TestCase):
    @httmock.all_requests
    def team_mock(self, url, request):
        return open('test_data/team.html').read()

    def test_team(self):
        expected = {'abbr': u'DIX',
                    'league': u'while(atCAE){doWork = false;}',
                    'name': u'LOL Clinton-Dix ',
                    'owner': u'Josh Gachnang',
                    'opponent': "Gordon's Cars  'N Cannabis  (Dan Siegler)",
                    'position': u'3rd',
                    'record': u'1-0'}
        with httmock.HTTMock(self.team_mock):
            team_data = team.scrape(1, 1, 2014)
        self.assertEqual(expected, team_data)


if __name__ == '__main__':
    unittest.main()
