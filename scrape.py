import requests
import re
from bs4 import BeautifulSoup
import json

card_rarity_enum = [
  "Bronze",
  "Silver",
  "Gold",
  "Diamond",
]
title_pattern = re.compile(r"Category:(" + "|".join(card_rarity_enum) + ")")
result = {}
all_card_rarities={}
all_combo_card_stats={}

def add_rarity(object, rarity, card, combo):
  combo_object = {
      "combo": combo,
      "combo_rarity": rarity,
    }
  if(card in object):
    object[card] = combo_object
  else:
    object[card] = {}
    object[card] = combo_object

def add_inital_card(object_card, subject_card, result, rarity, combo):
  if(object_card in result):
    add_rarity(result[object_card], rarity, subject_card, combo)
  else:
    result[object_card] = {}
    add_rarity(result[object_card], rarity, subject_card, combo)

def check_card_added_to_rarity(card):
  if(card not in all_card_rarities):
    card_rarity = get_card_rarity(card)
    all_card_rarities[card] = card_rarity

def get_card_rarity(card):
  card_response = requests.get(base_url + card.replace(" ", "_"))
  soup_card = BeautifulSoup(card_response.text, 'html.parser')
  card_rarity = soup_card.find('a', title=title_pattern).get_text()
  return card_rarity

def get_combo_card_stats(card):
  if(card == "Castle"):
    card = "Castle_(Card)"
  card_response = requests.get(base_url + card.replace(" ", "_"))
  print("request", base_url + card.replace(" ", "_"))
  soup_card = BeautifulSoup(card_response.text, 'html.parser')
  article_table = soup_card.find('table', class_='article-table')
  second_tr = article_table.find_all('tr')[1]
  td_elements = second_tr.find_all('td')
  attack = td_elements[0].get_text(strip=True)
  defense = td_elements[1].get_text(strip=True)
  return {
    "attack": attack,
    "defense": defense
    }

def check_card_added_to_combo(combo):
  if(combo not in all_combo_card_stats):
    stats = get_combo_card_stats(combo)
    all_combo_card_stats[combo] = {
      "attack": stats["attack"],
      "defense": stats["defense"]
      }

use_existing_data_for_rarities = input("Use existing data for card rarities: [y/n]")
if (use_existing_data_for_rarities == "y"):
  with open("all_card_rarities.json", "r") as json_file:
    all_card_rarities = json.load(json_file)

use_existing_data_for_combo = input("Use existing data for combo cards: [y/n]")
if (use_existing_data_for_combo == "y"):
  with open("all_card_rarities.json", "r") as json_file:
    all_card_rarities = json.load(json_file)

for rarity in card_rarity_enum:
  base_url = 'https://lil-alchemist.fandom.com/wiki/'
  url = base_url + "Card_Combinations/" + rarity

  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        links = row.find_all('a')

        if len(links) > 0:
          card1 = links[0].get_text()
          card2 = links[1].get_text()
          combo = links[2].get_text()
          
          if(use_existing_data_for_rarities != "y"):
            check_card_added_to_rarity(card1)
            check_card_added_to_rarity(card2)
          if(use_existing_data_for_combo != "y"):
            check_card_added_to_combo(combo)

          add_inital_card(card1, card2, result, rarity, combo)
          add_inital_card(card2, card1, result, rarity, combo)

json_data = json.dumps(result, ensure_ascii=False)
with open("data.json", "w") as json_file:
  json_file.write(json_data)

json_data = json.dumps(all_card_rarities, ensure_ascii=False)
with open("all_card_rarities.json", "w") as json_file:
  json_file.write(json_data)

json_data = json.dumps(all_combo_card_stats, ensure_ascii=False)
with open("all_card_combo_stats.json", "w") as json_file:
  json_file.write(json_data)