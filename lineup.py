import logging
import sys

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


attr_map = {
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


class Player(object):
    def __init__(self):
        pass

    @classmethod
    def from_content_row(cls, content_row, headers):
        player = cls()
        for child, header in zip(content_row.children, headers):
            if header:
                # Special casing for name/pos
                if header == 'PLAYER, TEAM POS':
                    player_name = list(child.children)[0].string.strip()
                    if not player_name:
                        raise InvalidPlayerRow('Could not parse a player name')
                    setattr(player, 'name', player_name)
                    pos = list(child.children)[1].split()
                    if len(pos) == 1:
                        setattr(player, attr_map['TEAM'], None)
                        setattr(player, attr_map['POS'], pos[0])
                    elif len(pos) == 3:
                        setattr(player, attr_map['TEAM'], pos[1])
                        setattr(player, attr_map['POS'], pos[2])
                else:
                    setattr(player, attr_map[header], child.string)
        return player


def scrape(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return get_players(soup)


def get_headers(row):
    """Given a subheader in the player table, return a list of column names"""
    return [header.string
            for header in row.children]


def get_players(soup):
    # Get all the rows in the player table
    table = soup.find('table', 'playerTableTable')
    rows = table.find_all('tr')
    players = []
    # Grab all the headers so we can match stats to names
    headers = get_headers(rows[1])
    # Skip first 2 rows (headers)
    for row in rows[2:]:
        if 'pncPlayerRow' in row.attrs['class']:
            try:
                players.append(Player.from_content_row(row, headers))
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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: lineup.py <URL>'
        sys.exit(-1)
    ps = scrape(sys.argv[1])
    for player in ps:
        print player.name, player.position, player.team, player.slot
