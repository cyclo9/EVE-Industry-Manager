extends LineEdit

signal calculate_cost

func _unhandled_input(event):
	if event is InputEventKey:
		if has_focus() and event.keycode == KEY_ENTER:
			calculate_cost.emit()
			set_text('1')
