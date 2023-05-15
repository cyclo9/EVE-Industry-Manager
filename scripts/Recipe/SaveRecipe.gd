extends Button

var item_name
var recipe

func _on_item_name_text_send_item_name(itm):
	item_name = itm

func _on_recipe_text_send_recipe(r):
	recipe = r

func _on_pressed():
	if FileAccess.file_exists('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()})):
		var dir = DirAccess.open('user://data/recipes')
		dir.remove('{item_name}'.format({'item_name': item_name.to_lower()}))
	
	var file = FileAccess.open('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()}), FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(recipe, '\t'))
		print('Write saved successfully')
	else:
		print('Write failed to save.')
