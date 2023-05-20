extends TextEdit

var modules = preload('res://scripts/modules.gd')

# Nodes
var Dashboard
var ItemText
var MaterialsReqText
var MaterialsNeededText

# Variables
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
		
func calc_mats_req(items_dict: Dictionary):
	var stack: Array = []
	for item in items_dict:
		var target_file: String = '{}.json'.format({'': item.to_lower()})
		var quantity = items_dict[item] # how many to make
		var output: int # how many of the selected item is produced per run
		if FileAccess.file_exists('user://data/recipes/{}'.format({'': target_file})):
			stack.append(target_file)
			var recipe = modules.json_to_dict(target_file)
			output = recipe['Runs'] # how many is made per run
			for ingredient in recipe['Data']:
				stack.append('{}.json'.format({'': ingredient}))
		else:
			print('Item(s) not found.')
			
		while stack:
			var current_file = stack.pop_back() # select the last item in the stack
			if FileAccess.file_exists('user://data/recipes/{}'.format({'': current_file})):
				var current_ingredient = modules.title(current_file.split('.json')[0])
				mats_req.erase(current_ingredient) # remove the current item from list of required materials
				var recipe = modules.json_to_dict(current_file)
				for ingredient in recipe['Data']:
					stack.append('{}.json'.format({'': ingredient}))
					var input = recipe['Data'][ingredient] # the amount of ingredients used to run 1 job of the selected item
					var multiplier = ceil(float(quantity) / float(output))
					var amount: int = input * multiplier
					if mats_req.has(ingredient): # you want to add onto the existing sum of the same ingredient
						mats_req[ingredient] += amount
					else:
						mats_req[ingredient] = amount

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
	
	calc_mats_req(items)
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
