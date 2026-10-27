extends SceneTree
func _initialize():call_deferred("run")
func run():
	var scene=load("res://main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await create_timer(.5).timeout
	var output=OS.get_environment("ENERGYBLAST_CAPTURE")
	DirAccess.make_dir_recursive_absolute(output)
	root.get_texture().get_image().save_png(output+"/menu.png")
	scene.voice.enabled=false
	scene.start_mission(0)
	scene.select_mode("aim")
	scene.aim=Vector2(8.5,-11.9).normalized()
	await create_timer(.4).timeout
	root.get_texture().get_image().save_png(output+"/bank.png")
	scene.start_mission(1)
	await create_timer(1).timeout
	root.get_texture().get_image().save_png(output+"/guardian.png")
	print("CAPTURE: 3 real frames saved")
	scene.voice.end_all()
	await create_timer(.15).timeout
	scene.queue_free()
	await process_frame
	await process_frame
	quit()
