extends TabContainer

var dir = DirAccess.open('user://data')

func _ready():
	if not dir.dir_exists('user://data'):
		dir.make_dir('user://data')
	if not dir.dir_exists('user://data/recipes'):
		dir.make_dir('user://data/recipes')
	if not dir.dir_exists('user://data/jobs'):
		dir.make_dir('user://data/jobs')
