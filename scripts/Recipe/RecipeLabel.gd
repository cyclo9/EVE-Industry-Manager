extends Label

@export var recipe_name: String

# Called when the node enters the scene tree for the first time.
func _ready():
	if recipe_name != '':
		text = recipe_name
