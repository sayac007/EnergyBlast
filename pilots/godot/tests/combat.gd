extends SceneTree
const P=preload("res://core/progress.gd")
var checks=0
var failures=[]
func check(value:bool,message:String):
	checks+=1
	if not value:failures.append(message);push_error(message)
func step(scene,seconds):
	for i in range(int(seconds/.025)):scene._process(.025)
func _initialize():call_deferred("run")
func run():
	var scene=load("res://main.tscn").instantiate();root.add_child(scene);await process_frame;scene.set_process(false);scene.voice.enabled=false
	var path="user://combat-test-"+str(OS.get_process_id())+".json";scene.progress=P.new(scene.definition,path);scene.start_mission(0)
	check(scene.turrets.size()==1 and scene.turrets[0].hp==2,"Live shielded cannon in first sector")
	check(scene.player.find_children("*","MeshInstance3D",true,false).size()>10,"Original detailed hero imported")
	check(scene.hp==3,"Fresh three-unit combat energy")
	var touch=InputEventScreenTouch.new();touch.index=0;touch.pressed=true;touch.position=scene.camera.unproject_position(Vector3(-4,0,2));scene._unhandled_input(touch);touch.pressed=false;scene._unhandled_input(touch)
	check(not scene.route.is_empty(),"Single tap moves without selecting a mode")
	scene.route=PackedVector2Array();scene.player_pos=Vector2(3,2);scene.aim=(scene.turrets[0].position-scene.player_pos).normalized();scene.shoot();step(scene,.4)
	check(scene.turrets[0].hp==2,"Direct shot cannot defeat front shield")
	scene.start_mission(0);scene.player_pos=Vector2(4.5,3.2);step(scene,1)
	check(scene.turrets[0].warning>0,"Enemy visibly charges and locks aim")
	var locked=scene.turrets[0].direction;scene.player_pos=Vector2(3.5,3.2);step(scene,.2)
	check(scene.turrets[0].direction==locked,"Charge does not invisibly track evasive movement")
	scene.player_pos=Vector2(4.5,3.2);step(scene,1.6)
	check(scene.damage_taken>0 and scene.hp<3,"Enemy projectile can actually hit player")
	var hp=scene.hp;scene.damage_player();check(scene.hp==hp,"Hit invulnerability prevents same-frame energy drain")
	scene.start_mission(0);step(scene,4)
	check(scene.hp==3,"Real cover intercepts enemy shells")
	check(scene.progress.total()==0,"Waiting never earns combat stars")
	scene.aim=Vector2(8.5,-11.9).normalized();scene.shoot();step(scene,1.8)
	check(scene.turrets[0].hp==1,"Visible moving player bolt damages cannon after bounce")
	scene.shoot();step(scene,1.8)
	check(scene.turrets[0].hp==0 and scene.mission_solved,"Second bank shot secures sector")
	check(scene.progress.total()==100 and scene.progress.hint_count()==2,"Combat result pays once and earns clues")
	scene.if_all_destroyed();check(scene.progress.total()==100,"No duplicate win award")
	var p=P.new(scene.definition,path);check(p.total()==100,"New combat stars persist")
	scene.start_mission(0);scene.navigate(Vector2(-3,3.2));scene.dash();check(scene.dash_left>0 and scene.invulnerable>0,"Dash acts immediately with short protection")
	var timer=scene.dash_cooldown;scene.dash();check(scene.dash_cooldown==timer,"Dash cooldown cannot be bypassed")
	scene.invulnerable=0;scene.hp=1;scene.damage_player();check(scene.combat_over and scene.popup.visible,"Defeat offers immediate sector restart")
	check(scene.progress.total()==100,"Defeat keeps accumulated stars")
	scene.start_mission(1);check(scene.turrets.size()==2 and scene.hp==3,"Second sector has two independently attacking cannons")
	scene.fire_held=true;scene.pointer_down=true;scene.active_touch=0;scene._notification(NOTIFICATION_APPLICATION_PAUSED)
	check(not scene.fire_held and not scene.pointer_down and scene.active_touch==-1,"Background transition cancels held fire and stale touch")
	scene._notification(NOTIFICATION_APPLICATION_RESUMED)
	var legacy_path="user://migration-"+str(OS.get_process_id())+".json"
	var old_definition=JSON.parse_string(FileAccess.get_file_as_string("res://assets/pilot.json"));var old=P.new(old_definition,legacy_path)
	old.award("mission:bank");old.award("skill:bank");old.buy_clue("bank")
	var migrated=P.new(scene.definition,legacy_path)
	check(migrated.total()==100 and migrated.hint_count()==1 and migrated.clue_level("bank")==1,"Version 0.1 stars, unlocked weapon and paid clue survive migration")
	check(migrated.award("mission:reactor")==75 and migrated.total()==175,"New combat rewards add to legacy balance")
	for name in [legacy_path,legacy_path+".bak"]:
		if FileAccess.file_exists(name):DirAccess.remove_absolute(ProjectSettings.globalize_path(name))
	scene.voice.end_all();scene.queue_free();await process_frame;await process_frame
	for name in [path,path+".bak"]:
		if FileAccess.file_exists(name):DirAccess.remove_absolute(ProjectSettings.globalize_path(name))
	print("SHOOTER: ",checks," checks; ",failures.size()," failures");quit(0 if failures.is_empty() else 1)
