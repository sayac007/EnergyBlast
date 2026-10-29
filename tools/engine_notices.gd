extends SceneTree
func _initialize():
	var base=ProjectSettings.globalize_path("res://assets/")
	var file=FileAccess.open(base+"GODOT_LICENSE.txt",FileAccess.WRITE)
	file.store_string(Engine.get_license_text());file.close()
	file=FileAccess.open(base+"GODOT_THIRD_PARTY.txt",FileAccess.WRITE)
	file.store_string(JSON.stringify(Engine.get_copyright_info(),"  ")+"\n\n"+JSON.stringify(Engine.get_license_info(),"  "));file.close()
	print("Godot compiled-engine and third-party notices saved")
	quit()
