extends TextEdit

signal add_recipe

var Dashboard

func _ready():
	Dashboard = get_node("../../../../Dashboard")
	
var item_name: String
var runs: int

func parse_recipe(recipe_text: String) -> Dictionary:
	var content: Array = recipe_text.split('\n')
	# Eliminates the "Time per run" line
	content.remove_at(0)
	
	item_name = content[0].split(' x ')[1]
	runs = content[0].split(' x ')[0].to_int()
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
	var recipe = parse_recipe(text)
	
	var dir = DirAccess.open('user://data/recipes')
	# This prevents the application from saving an empty file
	if dir != null and !recipe.is_empty():
		if FileAccess.file_exists('user://data/recipes/{}.json'.format({'': item_name.to_lower()})):
			dir.remove('{}'.format({'': item_name.to_lower()}))
		
		var file = FileAccess.open('user://data/recipes/{}.json'.format({'': item_name.to_lower()}), FileAccess.WRITE)
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
		
	set_text('')

func _input(event):
	if event is InputEventKey and event.pressed:
		if has_focus() and event.keycode == KEY_ENTER:
			if event.shift_pressed:
				save_recipe()

func _on_mouse_entered():
	Dashboard.set_mouse_filter(MOUSE_FILTER_IGNORE)

func _on_mouse_exited():
	Dashboard.set_mouse_filter(MOUSE_FILTER_PASS)
