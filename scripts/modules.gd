extends Node

static func json_to_dict(file_name: String):
	var file = FileAccess.open('user://data/recipes/{}'.format({'': file_name}), FileAccess.READ)
	return JSON.parse_string(file.get_as_text())
	
static func dict_to_multiline_str(dict: Dictionary):
	var string: String = ''
	for key in dict:
		string += '{qty} {itm} \n'.format({'qty': dict[key], 'itm': key})
	return string

static func title(string: String) -> String:
	var array: Array = string.split(' ')
	var new_array: Array = []
	for item in array:
		var word = item.split('')
		var new_word: Array = []
		for i in word.size():
			if i == 0:
				new_word.append(word[i].to_upper())
			else:
				new_word.append(word[i])
		var title_word = ''.join(new_word)
		new_array.append(title_word)
	var new_string = ' '.join(new_array)
	return new_string

static func generate_id(weight: int, start: int, end: int):
	var time = String.num(int(Time.get_unix_time_from_system()) * weight).split('')
	return ''.join(time.slice(start, end))
