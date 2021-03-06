import RAKE
import wikipediaapi
import shelve
import uuid

stop_dir = "SmartStoplist.txt" # list with wort for search keyphrase

def get_text_from_user():  # get text and save it in to file with unique name
	text = input('past or write text and press enter:')
	filename = uuid.uuid4()
	with open(f'text_{filename}.txt', 'w') as usf:
		usf.write(text)
	get_keyphrase(text, filename)

def get_keyphrase(user_text, unic_filename): # get keyphrase from text end send keywords list to saver
	rake_obj = RAKE.Rake(stop_dir)
	keywords = rake_obj.run(user_text)
	keyphrase_saver(keywords, unic_filename)

def keyphrase_saver(key_list, un_id): #save phrase list and chekc if exist wikipedia page for every single keyphrase
	with shelve.open(f"list_{un_id}") as keys:
		for key,score in key_list:
			wiki_exist = check_wiki_page_exst(key)
			keys[key]  = (score, wiki_exist)
	update_top_list(key_list)

def update_top_list(doc): # add keyphrase to top list or update it position if phrase already exist
	with shelve.open('top_list') as top:
		for key, _ in doc:
			top[key] = top.get(key, 0) + 1
			#print(key, top[key], _)

def check_wiki_page_exst(word): # check if keyphrase exist and return bool condition
	wiki_wiki  = wikipediaapi.Wikipedia('en')
	page_check = wiki_wiki.page(word)
	status     = page_check.exists()
	print(f"Page - Exists: {status} - {word}")
	return status

if __name__ == '__main__':
	get_text_from_user()