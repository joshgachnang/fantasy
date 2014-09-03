from bs4 import BeautifulSoup
import requests


def get_team_info(soup):
    container = soup.find_all('div', 'games-univ-mod3')[0]
    print container
    return {
        'name': list(container.find_all('h3', 'team-name')[0].children)[0],
        'abbr': list(container.find_all('h3', 'team-name')
                     [0].children)[1].string[1:-1],
        'league': list(container.children)[1].li.a.strong.string,
        'owner': container.find_all('li', 'per-info')[0].string
    }


def scrape(url):
    url = 'http://games.espn.go.com/ffl/clubhouse?leagueId=1441295' \
          '&teamId=2&seasonId=2014'
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return get_team_info(soup)
