# Creates a sqlite for each category

from sqlitedict import SqliteDict

splits = [i*10000000 for i in range(0, 8)]
source = './../data/sqlite/split_texts/'
path = "./../data/sqlite/community_texts/"
actual_category = "none"
category_dict = SqliteDict(f"{path}AL.sqlite", tablename="value", journal_mode="OFF")
text_dict = SqliteDict(f"{source}text_dict_{0}.sqlite", tablename="value", flag="r")

c = 0
for num in splits:
	category_dict.commit()
	text_dict.close()
	text_dict = SqliteDict(f"{source}text_dict_{num}.sqlite", tablename="value", flag="r")

	print(num)
	for id_c, value in text_dict.items():
		if value["category"] != actual_category:
			category_dict.commit()
			category_dict.close()
			category_dict = SqliteDict(f"{path}{value['category']}.sqlite", tablename="value", journal_mode="OFF")
			category_dict[id_c] = value

category_dict.commit()
category_dict.close()
