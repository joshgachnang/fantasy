from bs4 import BeautifulSoup
import requests


def get_team_info(soup):
    container = soup.find_all('div', 'games-univ-mod3')[0]
    data = {
        'name': list(container.find_all('h3', 'team-name')[0].children)[0],
        'abbr': list(container.find_all('h3', 'team-name')
                     [0].children)[1].string[1:-1],
        'league': list(container.children)[1].li.a.strong.string,
        'owner': container.find_all('li', 'per-info')[0].string
    }

    record = soup.find_all('div', 'games-univ-mod4')[0]
    data['position'] = list(record.find_all('em')[0])[0][1:-1]
    data['record'] = list(record.find_all('h4')[0].children)[1].strip()

    opponent = soup.find_all('div', 'games-univ-mod5')[0]
    data['opponent'] = list(opponent.find_all('li', 'games-firstlist')[0].children)[2].attrs['title']

    return data


def scrape(league_id, team_id, year):
    url = ('http://games.espn.go.com/ffl/clubhouse?leagueId={league}'
           '&teamId={team}&seasonId={year}'.format(**{
        'league': league_id,
        'team': team_id,
        'year': year
    }))
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    return get_team_info(soup)
