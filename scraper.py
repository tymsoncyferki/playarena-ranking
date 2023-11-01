import requests
from bs4 import BeautifulSoup
from app import Player, db, app
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def remove_quotes(input_string):
    if (input_string.startswith("'") and input_string.endswith("'")) \
            or (input_string.startswith('"') and input_string.endswith('"')):
        return input_string[1:-1]
    else:
        return input_string


def get_image_url(content):
    i_tag = content.find('i', id='user_avatar_image')
    style_attr = i_tag['style']
    image = style_attr.split('url(')[1].rstrip(')')
    image = remove_quotes(image)
    image_url = "https://playarena.pl" + image
    return image_url


def fix_player_image(url=None, content=None):
    assert url or content
    if not content:
        page = requests.get(url)
        content = BeautifulSoup(page.text, 'html.parser')
    player_image = get_image_url(content)
    player_id = re.search(r'(\d+)', url).group(1)
    player = Player.query.filter_by(id=player_id).first()
    if player:
        player.image = player_image
        db.session.commit()


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
    print(player)


def get_team_members_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    link = driver.find_element(By.XPATH, "//a[@id='ajax_team_members']")
    link.click()
    time.sleep(0.5)
    return driver.page_source


def scrape_team(url):
    page = get_team_members_content(url)
    content = BeautifulSoup(page, 'html.parser')
    team_name = content.find('div', {'id': "team_name"}).findChild().text.strip()
    team_members = content.find('div', {'class': 'teamMembers'})
    team_members_tables = team_members.find_all('tbody')
    for table in team_members_tables:
        table_rows = table.find_all('tr')
        for row in table_rows:
            url = row.find('a', class_='c_default').get('href')
            player_url = "https://playarena.pl" + url
            scrape_player(player_url, team_name)
