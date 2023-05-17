extends LineEdit

var ItemNameText
var RecipeText
var Dashboard

signal add_recipe

func _ready():
	ItemNameText = get_node('../ItemNameText')
	RecipeText = get_node('../RecipeText')
	Dashboard = get_node("../../../../Dashboard")
	
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
	
func save_recipe():
	var item_name = ItemNameText.text
	var recipe = parse_recipe(RecipeText.text)

	var dir = DirAccess.open('user://data/recipes')
	# This prevents the application from saving no-name or no-content file
	# it however, does not prevent the user from saving the wrong name or content
	if dir != null and item_name != '' and !recipe.is_empty():
		if FileAccess.file_exists('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()})):
			dir.remove('{item_name}'.format({'item_name': item_name.to_lower()}))
		
		var file = FileAccess.open('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()}), FileAccess.WRITE)
		if file:
			file.store_string(JSON.stringify(recipe, '\t'))
			add_recipe.emit()
			print('Recipe save successful')
		else:
			print('Recipe failed to save.')
			
	ItemNameText.set_text('')
	RecipeText.set_text('')
	
func _on_save_recipe_pressed():
	save_recipe()

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			save_recipe()
