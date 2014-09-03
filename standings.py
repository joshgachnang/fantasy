import sys

from bs4 import BeautifulSoup
import requests


attr_map = {
    'TEAM': 'name',
    'OWNER(S)': 'owner',
    'OWNER': 'owner',
    'STREAK': 'streak',
    'L': 'losses',
    'PCT': 'percentage',
    'PA': 'points_against',
    'PF': 'points_for',
    'GB': 'games_behind',
    'W': 'wins',
    'HOME': 'home_record',
    'DIV': 'division_record',
    'AWAY': 'away_record',
    'T': 'ties'
}


class Team(object):
    def __init__(self, name, owner=None, wins=None, losses=None, ties=None,
                 games_behind=None, points_for=None, points_against=None,
                 home_record=None, away_record=None, division_record=None,
                 streak=None, percentage=None):
        """
        :param name:
        :param owner:
        :param wins:
        :param losses:
        :param ties:
        :param games_behind:
        :param points_for:
        :param points_against:
        :param home_record:
        :param away_record:
        :param division_record:
        :param streak:
        :param percentage:
        :return:
        """
        self.name = name
        self.owner = owner
        self.wins = wins
        self.losses = losses
        self.ties = ties
        self.games_behind = games_behind
        self.points_for = points_for
        self.points_against = points_against
        self.home_record = home_record
        self.away_record = away_record
        self.division_record = division_record
        self.streak = streak
        self.percentage = percentage


def get_attrs(row, header):
    attrs = {}
    for attr, attr_name in zip(row.children, header):
        if attr_name:
            if attr_name == 'TEAM, OWNER(S)':
                # print 'ATTR', attr_name,
                # list(attr.children)[0].attrs['title']
                # print 'ATTR', attr_name, attr.a.attrs['title']
                attrs[attr_map['TEAM']] = attr.a.attrs['title'].split('(')[
                    0].strip()
                attrs[attr_map['OWNER']] = attr.a.attrs['title'].split('(')[
                    1].strip()
            elif attr_name in ['HOME', 'AWAY', 'DIV', 'STREAK']:
                # Special casing because .string was none
                attrs[attr_map[attr_name]] = attr.contents[1]
            else:

                attrs[attr_map[attr_name]] = attr.string
    return attrs


def get_headers(row):
    """Given a subheader in the player table, return a list of column names"""
    return [header.string
            for header in row.children]


def get_standings(soup):
    standings = {}
    tables = soup.find_all('table', 'tableBody')
    for table in tables:
        rows = table.find_all('tr')
        headers = get_headers(rows[1])
        for row in rows[2:]:
            attrs = get_attrs(row, headers)
            if attrs.get('name') not in standings:
                standings[attrs.get('name')] = {}
            standings[attrs.get('name')].update(attrs)
    return [Team(**kwargs) for kwargs in standings.values()]


def scrape(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return get_standings(soup)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: standings.py <URL>')
        sys.exit(-1)
