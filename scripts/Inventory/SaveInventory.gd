extends TextEdit

var json = JSON.new()
var Dashboard
var inventory: Dictionary

func _ready():
	Dashboard = get_node('../../../../Dashboard')
	
func parse_inventory():
	var content = text.split('\n')
	for line in content:
		var array = line.split('\t')
		if array.size() >=2:
			var item_name = array[0]
			var item_qty = int(array[1])
			inventory[item_name] = item_qty

func save_inventory():
	var file = FileAccess.open('user://data/inventory.json', FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(inventory, '\t'))
		print('Inventory save successful.')
	else:
		print('Inventory failed to save.')

func _on_text_changed():
	parse_inventory()
	save_inventory()

func _on_mouse_entered():
	Dashboard.set_mouse_filter(MOUSE_FILTER_IGNORE)

func _on_mouse_exited():
	Dashboard.set_mouse_filter(MOUSE_FILTER_PASS)
