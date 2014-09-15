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


def _get_attrs(row, header):
    attrs = {}
    for attr, attr_name in zip(row.children, header):
        if attr_name:
            if attr_name == 'TEAM, OWNER(S)':
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


def _get_headers(row):
    """Given a subheader in the player table, return a list of column names"""
    return [header.string
            for header in row.children]


def _get_standings(soup):
    standings = {}
    tables = soup.find_all('table', 'tableBody')
    for table in tables:
        rows = table.find_all('tr')
        headers = _get_headers(rows[1])
        for row in rows[2:]:
            attrs = _get_attrs(row, headers)
            if attrs.get('name') not in standings:
                standings[attrs.get('name')] = {}
            standings[attrs.get('name')].update(attrs)
    return standings.values()


def scrape(league_id,  year):
    url = "http://games.espn.go.com/ffl/standings?leagueId={league}" \
          "&seasonId={year}".format(league=league_id, year=year)
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return _get_standings(soup)
