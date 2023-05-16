extends Button

signal delete_recipe

var label

func _ready():
	label = get_node('../Label')

func _on_pressed():
	var recipe_name = label.text.to_lower()
	var recipe_file = String(recipe_name) + '.json'
	
	var dir = DirAccess.open('user://data/recipes')
	var error = dir.remove('user://data/recipes/{}'.format({'': recipe_file}))
	if error == OK:
		print('Recipe delete successful')
	else:
		print('Recipe failed to delete')
		print(recipe_file)
	dir.remove(recipe_file)
	delete_recipe.emit()
