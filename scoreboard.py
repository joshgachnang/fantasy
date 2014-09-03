from bs4 import BeautifulSoup
import requests


class Score(object):
    def __init__(self, name, points, owner=None, record=None, abbr=None,
                 position=None):
        """
        :param name:
        :param points:
        :param owner:
        :param record:
        :param abbr:
        :param position:
        :return:
        """
        self.name = name
        self.points = points
        self.owner = owner
        self.record = record
        self.abbr = abbr
        self.position = position


def get_scores(soup):
    standings = []
    # matchups = soup.select('#scoreboardMatchups')[0]
    # print(matchups)
    # matchups = soup.find_all('td', 'team')

    # print matchups
    tables = soup.find_all('div', 'scoreboardMatchups')
    # print(len(tables))
    for table in tables:
        # print table.attrs
        continue
        for row in table.find_all('tr'):
            attrs = {}
            name = row.find_all('div', 'name')[0]
            record = row.find_all('span', 'record')[0]
            owners = row.find_all('span', 'owners')[0]
            attrs['position'] = name.string
            attrs['name'] = name.a.string
            attrs['position'] = name.span.string
            attrs['record'] = record.string
            attrs['owner'] = owners.string
            standings.append(Score(**attrs))
    return standings


def scrape(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return get_scores(soup)
