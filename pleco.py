#!/usr/env python3
class PlecoCategory():
	def __init__(self, name, parent):
		self.name = name
		self.subcategories = []
		self.parent = parent
		self.cards = []

	def fullName(self):
		if self.parent == None:
			return '// '
		elif self.parent.fullName() == '// ':
			return self.parent.fullName() + self.name
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
		return True

	def export(self, filename):
		try:
			file = open(filename, "x")
		except FileExistsError:
			file = open(filename, "a")

		if self.name != "/" and len(self.cards) != 0:
			file.write(f'{self.fullName()}\n')
			file.close()
			for card in self.cards:
				card.export(filename)
		for subcategory in self.subcategories:
			subcategory.export(filename)

class PlecoFlashcard():
	def __init__(self, hanzi, pinyin, definition=''):
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
			if line != "":
				if "// " in line:
					path = [x.strip() for x in line[3:].split("/")]
					search = parser_object.catExists(path[0])
					if search == False:
						new_category = PlecoCategory(path[0], parser_object)
						parser_object.subcategories.append(new_category)
						current_category = new_category
					else:
						current_category = search
					if len(path) > 1:
						for category in path[1:]:
							search = parser_object.catExists(category)
							if search == False:
								new_category = PlecoCategory(category, current_category)
								current_category.subcategories.append(new_category)
								current_category = new_category
				elif "\t" in line:
					line = line.strip().split("\t")
					flashcard = PlecoFlashcard(line[0], line[1])#, line[2]#)
					current_category.cards.append(flashcard)
			else:
				current_category = parser_object
	return parser_object