#!/usr/env python3
class PlecoCategory():
	def __init__(self, name, parent):
		self.name = name
		self.subcategories = []
		self.parent = parent
		self.cards = []
		self.card_count = 0

	def fullName(self):
		if self.parent == None:
			return self.name
		else:
			return self.parent.fullName() + '/' + self.name

	def cardExists(self, card_obj):
		if getattr(card_obj, 'hanzi', None) == None and getattr(card_obj, 'pinyin', None) == None:
			raise TypeError("cardExists has been given an object without hanzi or pinyin attributes")
		if len(self.cards) == 0:
			return False
		for index, card in enumerate(self.cards):
			if card.hanzi == card_obj.hanzi:
				if card.pinyin == card_obj.pinyin:
					return index
		return False

	def catExists(self, category_name):
		if self.name == category_name:
			return self
		for category in self.subcategories:
			if category.name == category_name:
				return category
		for category in self.subcategories:
			subcat_search = category.catExists(category_name)
			if subcat_search != False:
				return subcat_search
		return False

	def remove(self, card):
		index = self.cardExists(card)
		if index == False:
			return False
		del self.cards[index]
		self.card_count -= 1
		return True

	def export(self, filename):
		try:
			file = open(filename, "x")
		except FileExistsError:
			file = open(filename, "a")

		file.write(f'{self.fullName()}\n')
		for card in self.cards:
			card.export(file)
		file.write('\n')
		for subcategory in self.subcategories:
			subcategory.export(file)

class PlecoFlashcard():
	def __init__(self, hanzi, pinyin, definition=None):
		try:
			index = hanzi.index('[')
			self.hanzi = hanzi[:index]
		except ValueError:
			self.hanzi = hanzi
		self.pinyin = pinyin
		self.definition = definition

	def export(self, filename):
		try:
			file = open(filename, "x")
		except FileExistsError:
			file = open(filename, "a")

		file.write(f'{self.hanzi}\t{self.pinyin}\t{self.definition}\n')

def plecoParser(filename):
	parser_object = PlecoCategory("/", None)
	with open(filename, "r") as file:
		current_category = parser_object
		for line in file.readlines():
			line = line.strip()
			if line != "":
				if line[:2] == "//":
					path = line[2:].split("/")
					for category in path:
						search = parser_object.catExists(category)
						if search == False:
							new_category = PlecoCategory(category, current_category)
							current_category.subcategories.append(new_category)
							current_category = new_category
						else:
							current_category = search
				elif "\t" in line:
					line = line.strip().split("\t")
					flashcard = PlecoFlashcard(line[0], line[1])#, line[2]#)
					current_category.cards.append(flashcard)
			else:
				current_category = parser_object
	return parser_object