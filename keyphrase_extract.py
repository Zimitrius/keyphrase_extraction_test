import RAKE
import wikipediaapi
import shelve
import uuid

stop_dir = "SmartStoplist.txt" # list with wort for search keyphrase


def get_text_from_user():  # get text and save it in to file with unique name
	text = input('copy or write text and press enter:')
	un_id = uuid.uuid4()
	filename = "text_{un_id}"
	with open(f'{filename}.txt', 'w') as f:
		f.write(text)
	get_keyphrase(text)


def get_keyphrase(user_text): # get keyphrase from text end send keywords list to saver
	rake_obj = RAKE.Rake(stop_dir)
	keywords = rake_obj.run(user_text)
	keyphrase_saver(keywords)

"""	save phrase list and chekc if exist wikipedia page for every single keyphrase
	and update top list  """
def keyphrase_saver(key_list):
	filename = "text_{uuid.uuid4()}"
	with shelve.open(filename) as keys:
		for key,score in key_list:
			existing = check_wiki_page_exst(key)
			keys[key] = (key, existing)
	update_top_list(key_list)


def update_top_list(doc): # add keyphrase to top list or update it position if phrase already exist
	with shelve.open('top_list') as top:
		for key, _ in doc:
			top[key] = top.get(key, 0) + 1
			print(key, top[key])

def check_wiki_page_exst(word): # check if keyphrase exist and return bool condition
	wiki_wiki = wikipediaapi.Wikipedia('en')
	page_py = wiki_wiki.page(word)
	status = page_py.exists()
	print(f"Page - Exists: {status} - {word}")
	return status


if __name__ == '__main__':
	get_text_from_user()