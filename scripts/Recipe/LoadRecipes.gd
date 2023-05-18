extends Control

var recipe_scene = preload('res://scenes/recipe.tscn')
var modules = preload('res://scripts/modules.gd')

func _ready():
	load_recipes()

func load_recipes():
	# empty the control node first
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
		set_custom_minimum_size(Vector2(0, (num_recipes * 48)))
		for i in recipes_list.size():
			# get the recipe name
			var recipe_name = recipes_list[i].split('.json')[0]
			var recipe_instance = recipe_scene.instantiate()
			recipe_instance.get_child(0).set_text(modules.title(recipe_name))
			recipe_instance.get_child(1).connect('delete_recipe', _on_delete_recipe)
			recipe_instance.position = Vector2(10, (i * 48))
			add_child(recipe_instance)

func _on_add_recipe():
	load_recipes()

func _on_delete_recipe():
	load_recipes()
