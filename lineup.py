import logging
import sys

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

attr_map = {
    'NAME': 'name',
    'POS': 'position',
    'TEAM': 'team',
    'SLOT': 'slot',
    'PRK': 'player_rank',
    'PTS': 'points',
    'AVG': 'average',
    'LAST': 'last_points',
    'PROJ': 'projected_points',
    'OPRK': 'opponent_rank',
    '%ST': 'percent_starting',
    '%OWN': 'percent_own',
    '+/-': 'ownership_change',
}


class InvalidPlayerRow(ValueError):
    pass


def scrape(league_id, team_id, year):
    url = "http://games.espn.go.com/ffl/clubhouse?leagueId={league}&teamId=" \
          "{team}&seasonId={year}".format(**
          {'league': league_id,
           'team': team_id,
           'year': year})
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return _get_players(soup)


def _from_content_row(content_row, headers):
    data = {}
    for child, header in zip(content_row.children, headers):
        if header:
            # Special casing for name/pos
            if header == 'PLAYER, TEAM POS':
                player_name = list(child.children)[0].string.strip()
                if not player_name:
                    raise InvalidPlayerRow('Could not parse a player name')
                data['name'] = player_name
                pos = list(child.children)[1].split()
                if len(pos) == 1:
                    data[attr_map['TEAM']] = None
                    data[attr_map['POS']] = pos[0]
                elif len(pos) == 3:
                    data[attr_map['TEAM']] = pos[1]
                    data[attr_map['POS']] = pos[2]
            else:
                data[attr_map[header]] = child.string
    return data


def _get_headers(row):
    """Given a subheader in the player table, return a list of column names"""
    return [header.string
            for header in row.children]


def _get_players(soup):
    # Get all the rows in the player table
    table = soup.find('table', 'playerTableTable')
    rows = table.find_all('tr')
    players = []
    # Grab all the headers so we can match stats to names
    headers = _get_headers(rows[1])
    # Skip first 2 rows (headers)
    for row in rows[2:]:
        if 'pncPlayerRow' in row.attrs['class']:
            try:
                players.append(_from_content_row(row, headers))
            except InvalidPlayerRow:
                continue
        elif ('playerTableBgRowHead' in row.attrs['class'] or
                      'playerTableBgRowSubhead' in row.attrs['class']):
            # Ignore headers
            pass
        else:
            # Unknown row.
            logger.warning("Unknown row: ", row)

    return players
