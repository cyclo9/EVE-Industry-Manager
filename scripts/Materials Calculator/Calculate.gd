extends LineEdit

var modules = preload('res://scripts/modules.gd')

var ItemText
var MultiplierText

var MaterialsReqText
var MaterialsNeededText

var mats_req: Dictionary
var mats_missing: Dictionary

func _ready():
	ItemText = get_node('../ItemText')
	MultiplierText = get_node('../MultiplierText')
	
	MaterialsReqText = get_node('../../MaterialsRequired/MaterialsReqText')
	MaterialsNeededText = get_node('../../MaterialsNeeded/MaterialsNeededText')
	
func calc_mats_req():
	mats_req = {}
	var stack: Array = []
	var target_file: String = '{}.json'.format({'': ItemText.text.to_lower()})
	if FileAccess.file_exists('user://data/recipes/{}'.format({'': target_file})):
		stack.append(target_file)
		var recipe = modules.json_to_dict(target_file)
		for ingredient in recipe:
			stack.append('{}.json'.format({'': ingredient}))
	else:
		print('Item not found.')

	while stack:
		var current_file = stack.pop_back()
		if FileAccess.file_exists('user://data/recipes/{}'.format({'': current_file})):
			var current_ingredient = current_file.split('.json')[0].capitalize()
			mats_req.erase(current_ingredient)
			var recipe = modules.json_to_dict(current_file)
			for ingredient in recipe:
				stack.append('{}.json'.format({'': ingredient}))
				var multiplier = int(MultiplierText.text)
				mats_req[ingredient] = int(recipe[ingredient]) * multiplier

func calc_mats_missing():
	mats_missing = {}
	if FileAccess.file_exists('user://data/inventory.json'):
		var file = FileAccess.open('user://data/inventory.json', FileAccess.READ)
		var inventory = JSON.parse_string(file.get_as_text())
		for ingredient in mats_req:
			if ingredient in inventory:
				var qty_missing = mats_req[ingredient] - inventory[ingredient]
				if qty_missing > 0:
					mats_missing[ingredient] = qty_missing
			else:
				mats_missing[ingredient] = mats_req[ingredient]
	
func update():
	calc_mats_req()
	calc_mats_missing()
	
	MaterialsReqText.set_text(modules.dict_to_multiline_str(mats_req))
	MaterialsNeededText.set_text(modules.dict_to_multiline_str(mats_missing))

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			update()

func _on_calculate_button_pressed():
	update()

func _on_multiplier_text_calculate_cost():
	update()
