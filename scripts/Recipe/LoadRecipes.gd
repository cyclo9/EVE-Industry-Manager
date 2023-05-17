extends Control

var recipe_scene = preload('res://scenes/recipe.tscn')

func title(string: String):
	var array: Array = string.to_lower().split(' ')
	var new_array: Array = []
	for item in array:
		var word: Array = item.split('')
		var title_word: String = ''
		for i in word.size():
			if i == 0:
				title_word += word[i].to_upper()
			else:
				title_word += word[i]
		new_array.append(title_word)

	var new_string: String = ''
	for i in new_array.size():
		if i == 0:
			new_string += new_array[i]
		else:
			new_string += ' ' + new_array[i]
	
	return new_string

func load_recipes():
	var children = get_children()
	for child in children:
		remove_child(child)
		child.queue_free()
	
	var dir = DirAccess.open('user://data/recipes')
	if dir != null:
		# gets a list of all the recipes
		var recipes_list = dir.get_files()
		var num_recipes: int = recipes_list.size()
		# expands the Control node to fit all the recipes
		set_custom_minimum_size(Vector2(600, (num_recipes * 38)))
		for i in recipes_list.size():
			# get the recipe name
			var recipe_name = recipes_list[i].split('.json')[0]
			var recipe_instance = recipe_scene.instantiate()
			recipe_instance.get_child(1).connect('delete_recipe', _on_delete_recipe)
			recipe_instance.get_child(0).set_text(title(recipe_name))
			recipe_instance.position = Vector2(10, (i * 35))
			add_child(recipe_instance)

# Called when the node enters the scene tree for the first time.
func _ready():
	load_recipes()

func _on_add_recipe():
	load_recipes()

func _on_delete_recipe():
	load_recipes()
