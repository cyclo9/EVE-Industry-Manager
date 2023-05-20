extends LineEdit

var Dashboard
var RecipeText
var ItemNameText
var RunsText

signal add_recipe

func _ready():
	Dashboard = get_node("../../../../Dashboard")
	RecipeText = get_node('../RecipeText')
	ItemNameText = get_node('../ItemNameText')
	RunsText = get_node('../RunsText')
	
func parse_recipe(recipe_text: String) -> Dictionary:
	var content: Array = recipe_text.split('\n')
	# Eliminates the "Time per run" line
	content.remove_at(0)
	var recipe: Dictionary = {}
	
	for line in content:
		var array = line.split(' x ')
		if array.size() >= 2:
			var item: String = array[1]
			var quantity: int = int(array[0])
			recipe[item] = quantity
			
	return recipe
	
func save_recipe():
	var recipe = parse_recipe(RecipeText.text)
	var item_name = ItemNameText.text
	var runs = int(RunsText.text)

	var dir = DirAccess.open('user://data/recipes')
	# This prevents the application from saving no-name or no-content file
	# it however, does not prevent the user from saving the wrong name or content
	if dir != null and item_name != '' and !recipe.is_empty():
		if FileAccess.file_exists('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()})):
			dir.remove('{item_name}'.format({'item_name': item_name.to_lower()}))
		
		var file = FileAccess.open('user://data/recipes/{item_name}.json'.format({'item_name': item_name.to_lower()}), FileAccess.WRITE)
		if file:
			var data: Dictionary = {
				'Runs': runs,
				'Data': recipe
			}
			file.store_string(JSON.stringify(data, '\t', false))
			add_recipe.emit()
			print('Recipe save successful.')
		else:
			print('Recipe failed to save.')
	else:
		print('Item Name/Recipe is/are empty.')
			
	ItemNameText.set_text('')
	RecipeText.set_text('')
	
func _on_save_recipe_pressed():
	save_recipe()
	
func _on_runs_text_save_recipe():
	save_recipe()

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			save_recipe()
