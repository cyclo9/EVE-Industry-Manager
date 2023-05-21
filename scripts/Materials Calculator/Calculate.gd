extends TextEdit

var modules = preload('res://scripts/modules.gd')

# Nodes
var Dashboard
var ItemText
var MaterialsReqText
var MaterialsNeededText

# Variables
var recipe_path: String = 'user://data/recipes/'
var items: Dictionary
var mats_req: Dictionary
var mats_missing: Dictionary

func _ready():
	Dashboard = get_node('../../../../Dashboard')
	ItemText = get_node('../ItemText')

	MaterialsReqText = get_node('../../MaterialsRequired/MaterialsReqText')
	MaterialsNeededText = get_node('../../MaterialsNeeded/MaterialsNeededText')
	
func parse_items():
	var array: Array = text.split('\n')
	for element in array:
		var quantity: int = int(element.split(' ')[0])
		var item: String = ' '.join(element.split(' ').slice(1))
		items[item] = quantity

func calc_mats_req(item, qty_to_make):
	var target_file: String = '{}.json'.format({'': item.to_lower()})
	if FileAccess.file_exists(recipe_path + '{}'.format({'': target_file})):
		var recipe = modules.json_to_dict(target_file)
		var output = recipe['Runs']
		for ingredient in recipe['Data']:
			var input: int = recipe['Data'][ingredient] # amount of ingredient per 1 run
			var multiplier: int = ceil(float(qty_to_make) / float(output))
			var amount: int = input * multiplier
			if mats_req.has(ingredient):
				mats_req[ingredient] += amount
			else:
				mats_req[ingredient] = amount
				
			mats_req.erase(item)
			calc_mats_req(ingredient, amount)

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
	# Clear variables
	items = {}
	mats_req = {}
	mats_missing = {}
	
	parse_items()
	
	for item in items:
		calc_mats_req(item, items[item])
	calc_mats_missing()
	
	MaterialsReqText.set_text(modules.dict_to_multiline_str(mats_req))
	MaterialsNeededText.set_text(modules.dict_to_multiline_str(mats_missing))

func _input(event):
	if event is InputEventKey and event.pressed:
		if has_focus() and event.keycode == KEY_ENTER:
			if event.shift_pressed:
				update()
	
func _on_mouse_entered():
	Dashboard.set_mouse_filter(MOUSE_FILTER_IGNORE)

func _on_mouse_exited():
	Dashboard.set_mouse_filter(MOUSE_FILTER_PASS)
