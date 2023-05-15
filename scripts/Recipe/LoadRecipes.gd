extends Control

var recipe_scene = preload('res://scenes/recipe.tscn')

func title(text: String) -> String:
	var words = text.split(' ')
	var string: String = ''
	for i in range(words.size()):
		if i == 0:
			words[i] = words[i].capitalize()
		else:
			words[i] = String(' ') + words[i].capitalize()
		string += String(words[i])
	return string
	
func load_recipes():
	var children = get_children()
	for child in children:
		remove_child(child)
		child.queue_free()
	
	var dir = DirAccess.open('user://data/recipes')
	# gets a list of all the recipes
	var recipes_list = dir.get_files()
	for i in recipes_list.size():
		# get the recipe name
		var recipe_name = recipes_list[i].split('.json')[0]
		var recipe_instance = recipe_scene.instantiate()
		recipe_instance.get_child(1).connect('delete_recipe', _on_delete_recipe)
		recipe_instance.get_child(0).set_text(title(recipe_name))
		recipe_instance.position = Vector2(10, (i * 35) + 10)
		add_child(recipe_instance)

# Called when the node enters the scene tree for the first time.
func _ready():
	load_recipes()

func _on_save_recipe_add_recipe():
	load_recipes()

func _on_delete_recipe():
	load_recipes()
