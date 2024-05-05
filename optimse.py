import json

with open("data.json", "r") as json_file:
    object_data = json.load(json_file)
with open("all_card_rarities.json", "r") as json_file:
    all_card_rarities = json.load(json_file)
with open("all_card_combo_stats.json", "r") as json_file:
    all_combo_stats = json.load(json_file)

def calculate_pref_total(attack, defense, rarity, total):
    if prefernce == 1:
        total += attack * prefernce["fav"] + defense * prefernce["les"] + rarity_pref[rarity]
    elif prefernce == 2:
        total += attack * prefernce["fav"] + defense * prefernce["les"] + rarity_pref[rarity]
    else:
        total += attack * prefernce["bal"] + defense * prefernce["bal"] + rarity_pref[rarity]
    return total

def main():
    for object in object_data:
        total = 0
        total_pref = 0
        bronze = 0
        silver = 0
        gold = 0
        diamond = 0
        for card in cards_you_want_to_match:
            if card in object_data[object]:
                if all_card_rarities[object] in only_want_card_rarity:
                    combo_card = object_data[object][card]["combo"]
                    combo_card_attack = int(all_combo_stats[combo_card]["attack"])
                    combo_card_defence = int(all_combo_stats[combo_card]["defense"])

                    total_pref += calculate_pref_total(combo_card_attack, combo_card_defence, object_data[object][card]["combo_rarity"], total_pref)
                    total += weighting[object_data[object][card]["combo_rarity"]]
                    if object_data[object][card]["combo_rarity"] == "Bronze":
                        bronze+=1
                    if object_data[object][card]["combo_rarity"] == "Silver":
                        silver+=1
                    if object_data[object][card]["combo_rarity"] == "Gold":
                        gold+=1
                    if object_data[object][card]["combo_rarity"] == "Diamond":
                        diamond+=1
            else:
                total += weighting["NoCombo"]

        result[object] = {
            "total": total,
            "pref": total_pref,
            "bronze": bronze,
            "silver": silver,
            "gold": gold,
            "diamond": diamond,
        }

    for card in cards_you_want_to_match:
        if card in result:
            del result[card]

    sorted_data = sorted(result.items(), key=lambda x: (x[1]['total'], x[1]['pref']), reverse=True)
    for item in sorted_data[:10]:
        print(item)

    json_data = json.dumps(sorted_data, ensure_ascii=False)
    with open("data-result.json", "w") as json_file:
        json_file.write(json_data)



print("Type for prefernce:")
print("Attack: 1")
print("Defense: 2")
print("Balance: 3")
user_preference = input()

print("Type to only show up to:")
print("Bronze: 1")
print("Silver: 2")
print("Gold: 3")
print("Diamond: 4")
show_rarity_preference = int(input())

only_want_card_rarity = ["Bronze"]

cards_you_want_to_match = []

weighting = {
    "NoCombo": -2,
    "Bronze": 1,
    "Silver": 3,
    "Gold": 6,
    "Diamond": 10
}
prefernce = {
    "fav": 0.7,
    "les": 0.3,
    "bal": 0.5
}
rarity_pref = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3,
    "Diamond": 4
}

result = {}

if show_rarity_preference > 1 :
    only_want_card_rarity.append("Silver")
if show_rarity_preference > 2 :
    only_want_card_rarity.append("Gold")
if show_rarity_preference > 3:
    only_want_card_rarity.append("Diamond")

while True:
    print('')
    print("Press 'q' to exit")
    print("Current cards you want to match:", cards_you_want_to_match)
    card_to_add = input("Add to your card array, or skip by pressing enter: ")
    if card_to_add == "q":
        break
    elif card_to_add != "":
        cards_you_want_to_match.append(card_to_add)
    main()