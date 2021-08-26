#!/usr/env python3
from pleco import *

deck = [plecoParser("/home/wyvern/Desktop/pleco/cards.txt")]
#totalCharacters = []
deckCharacters = []
results = {}

for category in deck:
	totalCount = 0
	subCharacters = []
	subCount = 0
	for card in category.cards:
		if len(card.hanzi) == 1:
			if card.hanzi not in totalCharacters:
				totalCharacters.append(card.hanzi)
				totalCount += 1
			if card.hanzi not in subCharacters:
				subCharacters.append(card.hanzi)
				subCount += 1
		elif len(card.hanzi) > 1:
			for character in card.hanzi:
				if character not in totalCharacters:
					totalCharacters.append(character)
					totalCount += 1
				if character not in subCharacters:
					subCharacters.append(character)
					subCount += 1
	results[category.name] = [totalCount, subCount, subCharacters]
	for subcategory in category.subcategories:
		deck.append(subcategory)

for name in results:
	print(f'Category <{name}> has {results[name][:2]} unique characters')

inter = results["中级 - Intermediate Level"][2]
adv = results["高级 - Advanced Level"][2]
sup = results["附录 - Supplemental Vocab"][2]
deck = results["/"][2]
freq = results[" Freq"][2]

for card in inter:
	if card in adv or card in sup or card in deck or card in freq:
		inter.remove(card)

for x in results:
	print(len(results[x][2]))