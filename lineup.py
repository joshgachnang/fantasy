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


class Player(object):
    def __init__(self, name, position, team=None, slot=None, player_rank=None,
                 points=None, average=None, last_points=None,
                 projected_points=None, opponent_rank=None,
                 percent_starting=None, percent_own=None,
                 ownership_change=None):
        """Create an object representing a single player

        :param name: Name of the player
        :param position: Player's position, abbreviated. e.g. 'QB'
        :param team:
        :param slot:
        :param player_rank:
        :param points:
        :param average:
        :param last_points:
        :param projected_points:
        :param opponent_rank:
        :param pecent_starting:
        :param percent_own:
        :param ownership_change:
        """
        self.name = name
        self.position = position
        self.team = team
        self.slot = slot
        self.player_rank = player_rank
        self.points = points
        self.average = average
        self.last_points = last_points
        self.projected_points = projected_points
        self.opponent_rank = opponent_rank
        self.percent_starting = percent_starting
        self.percent_own = percent_own
        self.ownership_change = ownership_change

    @classmethod
    def from_content_row(cls, content_row, headers):
        kwargs = {}
        for child, header in zip(content_row.children, headers):
            if header:
                # Special casing for name/pos
                if header == 'PLAYER, TEAM POS':
                    player_name = list(child.children)[0].string.strip()
                    if not player_name:
                        raise InvalidPlayerRow('Could not parse a player name')
                    kwargs['name'] = player_name
                    pos = list(child.children)[1].split()
                    if len(pos) == 1:
                        kwargs[attr_map['TEAM']] = None
                        kwargs[attr_map['POS']] = pos[0]
                    elif len(pos) == 3:
                        kwargs[attr_map['TEAM']] = pos[1]
                        kwargs[attr_map['POS']] = pos[2]
                else:
                    kwargs[attr_map[header]] = child.string
        return cls(**kwargs)


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
        print('Usage: lineup.py <URL>')
        sys.exit(-1)
    ps = scrape(sys.argv[1])
    for player in ps:
        print(player.name, player.position, player.team, player.slot)
