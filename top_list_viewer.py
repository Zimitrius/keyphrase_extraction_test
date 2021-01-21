import shelve

def view_top_list(): # top list viewer
	with shelve.open('top_list') as top:
		sorted_list = sorted(top, key = top.values, reverse=1)
	for key, value in sorted_list():
		print( f"{key} - {value}")

if __name__ == '__main__':
	view_top_list()