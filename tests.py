import unittest

import responses

import lineup


class TestLineup(unittest.TestCase):
    @responses.activate
    def test_soup(self):
        url = ('http://games.espn.go.com/ffl/clubhouse?leagueId=844419'
               '&teamId=8&seasonId=2013')
        responses.add(responses.GET, url,
                      body=open('test_data/hoyer_the_destroyed.html').read(),
                      status=404, content_type='text/html')
        players = lineup.scrape(url)
        for player in players:
            print player.name
        self.assertEqual(21, len(players))


if __name__ == '__main__':
    unittest.main()
