extends TextEdit

var json = JSON.new()

func save(content):
	var file = FileAccess.open('user://data/inventory.json', FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(content, '\t'))
		print('Write saved succesfully.')
	else:
		print('Write failed to save.')

func _on_text_changed():
	var content = text.split('\n')
	var inventory = {}
	
	for line in content:
		var array = line.split('\t')
		if array.size() >=2:
			var item_name = array[0]
			var item_qty = int(array[1])
			inventory[item_name] = item_qty
	
	save(inventory)
