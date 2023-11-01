import requests
from bs4 import BeautifulSoup
from app import Player, db, app
import re


def get_image_url(content):
    i_tag = content.find('i', id='user_avatar_image')
    style_attr = i_tag['style']
    image = style_attr.split('url(')[1].rstrip(')')
    image_url = "https://playarena.pl" + image
    return image_url


def scrape_player(url, team=None):
    page = requests.get(url)
    content = BeautifulSoup(page.text, 'html.parser')
    player_id = re.search(r'(\d+)', url).group(1)
    if Player.query.filter_by(id=player_id).first():
        print('Player already scraped')
        return
    player_name = content.find('div', {'id': 'user_name'}).text.strip()
    player_rank = content.find('div', class_='col-md-4 col-sm-12 text-center').find('span',
                                                                                    class_='rankCounter5').text.strip()
    player_image = get_image_url(content)
    player = Player(id=player_id, name=player_name, rank=player_rank, team=team, image=player_image)
    db.session.add(player)
    db.session.commit()
    print(Player.query.all())
    print(player)


def scrape_team(url):
    # todo: selenium
    team_url = url + "#members"
    page = requests.get(team_url)
    content = BeautifulSoup(page.text, 'html.parser')
    team_members = content.find('div', {'class': 'teamMembers'})
    team_members_tables = team_members.find_all('tbody')
    for table in team_members_tables:
        table_rows = table.find_all('tr')
        for row in table_rows:
            url = row.find('a', class_='c_default').get('href')
            print(url)
