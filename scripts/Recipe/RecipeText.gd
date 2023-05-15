extends TextEdit

signal send_recipe(recipe)
	
func parse_recipe():
	var content = text.split('\n')
	content.remove_at(0)
	var recipe = {}
	
	for line in content:
		var array = line.split(' x ')
		if array.size() >= 2:
			var item = array[1]
			var quantity = array[0]
			recipe[item] = quantity
			
	return recipe

func _on_save_recipe_pressed():
	send_recipe.emit(parse_recipe())
