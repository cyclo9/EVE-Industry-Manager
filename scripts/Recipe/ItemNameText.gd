extends LineEdit

signal send_item_name(item_name)

func _on_save_recipe_pressed():
	send_item_name.emit(text)
