extends LineEdit

signal save_recipe

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			save_recipe.emit()
			set_text('1')
