fantasy
=======

Tools for scraping fantasy stats, current Fantasy Football from ESPN.

Currently supports Python 2.7, 3.3, 3.4, and PyPy.

Released under MIT License

[![Build Status](https://travis-ci.org/pcsforeducation/fantasy.svg)](https://travis-ci.org/pcsforeducation/fantasy)


Scoreboard
----------

    from fantasy import scoreboard
    
    scoreboard.scrape(league_id=XXX, team_id=1, year=2014)
    
    >>> {'abbr': u'DIX',
         'league': u'The League',
         'name': u'LOL Clinton-Dix ',
         'owner': u'Josh Gachnang',
         'opponent': "Smoking Weeden (Brian Hoyer)",
         'position': u'3rd',
         'record': u'1-0'}

Standings
---------

    from fantasy import standings
    
    standings.scrape(league_id=XXX, year=2013)
    
    >>> [{'streak': u'W4',
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
         ...]
         
Lineup
------

    from fantasy import lineup
    
    lineup.scrape(league_id=XXX, team_id=1, year=2014

    >>> [{'slot': u'QB',
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
          'points': u'282.6'
        },
        ...]


Tests
-----

Tests are run using tox. 

    pip install tox
    
    tox