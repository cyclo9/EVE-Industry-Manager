extends Button

var ItemNameText
var RecipeText

signal add_recipe

func _ready():
	ItemNameText = get_node('../ItemNameText')
	RecipeText = get_node('../RecipeText')
	
func parse_recipe(recipe_text):
	var content = recipe_text.split('\n')
	# Eliminates the "Time per run" line
	content.remove_at(0)
	var recipe = {}
	
	for line in content:
		var array = line.split(' x ')
		if array.size() >= 2:
			var item = array[1]
			var quantity = array[0]
			recipe[item] = quantity
			
	return recipe

func _on_pressed():
	var item_name = ItemNameText.text
	var recipe = parse_recipe(RecipeText.text)

	if FileAccess.file_exists('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()})):
		var dir = DirAccess.open('user://data/recipes')
		dir.remove('{item_name}'.format({'item_name': item_name.to_lower()}))
	
	var file = FileAccess.open('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()}), FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(recipe, '\t'))
		add_recipe.emit()
		print('Write saved successfully')
	else:
		print('Write failed to save.')
