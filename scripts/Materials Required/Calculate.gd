extends LineEdit

var ItemText
var MultiplierText
var MaterialsReqText

@export var materials_req: Dictionary = {}

func _ready():
	ItemText = get_node('../ItemText')
	MultiplierText = get_node('../MultiplierText')
	MaterialsReqText = get_node('../MaterialsReqText')
	
func json_to_dict(file_name: String):
	var file = FileAccess.open('user://data/recipes/{}'.format({'': file_name}), FileAccess.READ)
	return JSON.parse_string((file.get_as_text()))
	
func dict_to_multiline_str(dict: Dictionary):
	var string: String = ''
	for key in dict:
		string += '{qty} {itm} \n'.format({'qty': dict[key], 'itm': key})
	return string
	
func calculate():
	var stack: Array = []
	var target_file: String = '{}.json'.format({'': ItemText.text.to_lower()})
	if FileAccess.file_exists('user://data/recipes/{}'.format({'': target_file})):
		stack.append(target_file)
		var recipe = json_to_dict(target_file)
		for ingredient in recipe:
			stack.append('{}.json'.format({'': ingredient}))
	else:
		print('Item not found.')
		
	while stack:
		var current_file = stack.pop_back()
		if FileAccess.file_exists('user://data/recipes/{}'.format({'': current_file})):
			var current_ingredient = current_file.split('.json')[0].capitalize()
			materials_req.erase(current_ingredient)
			var recipe = json_to_dict(current_file)
			for ingredient in recipe:
				stack.append('{}.json'.format({'': ingredient}))
				var multiplier = int(MultiplierText.text)
				materials_req[ingredient] = int(recipe[ingredient]) * multiplier
				
	MaterialsReqText.set_text(dict_to_multiline_str(materials_req))

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			calculate()

func _on_calculate_button_pressed():
	calculate()

func _on_multiplier_text_calculate_cost():
	calculate()
