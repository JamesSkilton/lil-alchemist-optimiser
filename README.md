# Lil alchemist optimiser

## Scrape
The data is scraped from the [Little Alhemist wiki](https://lil-alchemist.fandom.com/wiki/), it will get all combinations from each rarity and dump them into three files:

### [all_card_combo_stats](./all_card_combo_stats.json):
This contains attack and defence of the `F` cards that are created as a result of joining two combo cards together.

### [all combo card rarities](./all_card_rarities):
This contains the rarities of each combo card

### [data](./data.json):
This contains a list of the cards that can be combo'd together.
#### Note: this shouldn't contain attack and defence

### Running it:
When running the scrape it will give you the option to use the existing data or not

## Optimser
This will use all the three files above to list the top 10 cards that would be best to add your deck.

### Running it
When this is ran it will ask you whether you want a more attacking, defensive or balanced deck, this choice will change how the `pref` is calculated. 

The second thing it will ask you is what rarity of card do you want it to recommend.

#### `pref` 
The higher this number the more it aligns with your preference
|Type|Multiple|
|-|-|
|Fav|0.7|
|Less|0.3|
|Balance|0.5|

#### `total`
The higher this number the more likly the combinations are better
|Rarity|Weighting|
|-|-|
|No combo|-2|
|Bronze|1|
|Silver|3|
|Gold|6|
|Diamond|10|


