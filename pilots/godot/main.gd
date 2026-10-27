extends Node3D
const Geometry = preload("res://core/geometry.gd")
const Progress = preload("res://core/progress.gd")
const Icon = preload("res://core/icon_button.gd")
const Voice = preload("res://core/voice.gd")
const Overlay = preload("res://core/overlay.gd")
var definition: Dictionary
var progress: PilotProgress
var mission: Dictionary
var player_pos = Vector2.ZERO
var guardian_pos = Vector2.ZERO
var guardian_forward = Vector2.RIGHT
var guardian_index = 0
var player: Node3D
var guardian: Node3D
var camera: Camera3D
var world: Node3D
var cone: MeshInstance3D
var secret: Node3D
var goal: Node3D
var gate: Node3D
var trap_node: Node3D
var voice: PilotVoice
var menu_panel: PanelContainer
var popup: PanelContainer
var overlay: Control
var stars_label: Label
var hints_label: Label
var status_label: Label
var mode_buttons = {}
var gate_lights = []
var route = PackedVector2Array()
var prediction = null
var aim = Vector2(1,-1).normalized()
var mode = "move"
var clock = 0.0
var trap_pos = null
var trap_life = 0.0
var trap_used = false
var guard_frozen = 0.0
var awareness = 0.0
var detected_count = 0
var shots = 0
var trace_left = 0.0
var last_trace = []
var shot_pending = false
var pending_win = false
var pending_skill = false
var retry_left = 0.0
var complete = false
var mission_solved = false
var clue_visible = 0.0
var clue_cooldown = 0.0
var walls = []
var buttons_box: HBoxContainer
var backgrounded = false

func _ready():
	definition = JSON.parse_string(FileAccess.get_file_as_string("res://assets/pilot.json"))
	progress = Progress.new(definition)
	setup_environment()
	setup_ui()
	load_mission(0)
	show_menu()

func material(color: Color, glow: bool = false) -> StandardMaterial3D:
	var m = StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = .8
	if glow:
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	return m

func box(parent: Node3D, pos: Vector3, size: Vector3, color: Color) -> MeshInstance3D:
	var node = MeshInstance3D.new()
	var mesh = BoxMesh.new()
	mesh.size = size
	node.mesh = mesh
	node.material_override = material(color)
	node.position = pos
	parent.add_child(node)
	return node

func sphere(parent: Node3D, pos: Vector3, radius: float, color: Color) -> MeshInstance3D:
	var node = MeshInstance3D.new()
	var mesh = SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius*2
	node.mesh = mesh
	node.material_override = material(color,true)
	node.position = pos
	parent.add_child(node)
	return node

func setup_environment():
	var environment = WorldEnvironment.new()
	var env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("102334")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("b8d8e8")
	env.ambient_light_energy = .45
	environment.environment = env
	add_child(environment)
	var light = DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-60,-30,0)
	light.light_energy = 1.0
	light.shadow_enabled = true
	add_child(light)
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.position = Vector3(0,19,13)
	add_child(camera)
	camera.look_at(Vector3.ZERO)
	camera.current = true
	get_viewport().size_changed.connect(fit_camera)
	fit_camera()

func fit_camera():
	var viewport = get_viewport().get_visible_rect().size
	var aspect = viewport.x / maxf(1,viewport.y)
	camera.keep_aspect = Camera3D.KEEP_HEIGHT
	camera.size = maxf(11.5, 15.8 / aspect)

func style(color: Color, radius: int = 20) -> StyleBoxFlat:
	var s = StyleBoxFlat.new()
	s.bg_color = color
	s.set_corner_radius_all(radius)
	s.content_margin_left = 14
	s.content_margin_right = 14
	s.content_margin_top = 10
	s.content_margin_bottom = 10
	return s

func label(text: String, size: int = 24) -> Label:
	var l = Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size",size)
	l.add_theme_color_override("font_color",Color("ebfff7"))
	return l

func button(text: String, id: String, parent: Node, callback: Callable) -> Button:
	var b = Icon.new()
	b.icon_id = id
	b.text = "\n\n"+text
	b.add_theme_stylebox_override("normal",style(Color("203f55")))
	b.add_theme_stylebox_override("pressed",style(Color("47726d")))
	b.add_theme_stylebox_override("hover",style(Color("31586d")))
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(b)
	b.pressed.connect(callback)
	return b

func setup_ui():
	var canvas = CanvasLayer.new()
	add_child(canvas)
	var root = Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	canvas.add_child(root)
	overlay = Overlay.new()
	overlay.game = self
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(overlay)
	var top = HBoxContainer.new()
	top.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	top.offset_left=20;top.offset_right=-20;top.offset_top=16
	root.add_child(top)
	stars_label = label("",32)
	stars_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top.add_child(stars_label)
	hints_label = label("",22)
	top.add_child(hints_label)
	button("Karten","play",top,show_menu).custom_minimum_size=Vector2(84,76)
	button("Ton","sound",top,func(): voice.toggle()).custom_minimum_size=Vector2(76,76)
	var bottom = VBoxContainer.new()
	bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.offset_left=16;bottom.offset_right=-16;bottom.offset_top=-220;bottom.offset_bottom=-18
	root.add_child(bottom)
	status_label=label("",22)
	status_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	status_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	status_label.custom_minimum_size.y=50
	bottom.add_child(status_label)
	buttons_box=HBoxContainer.new()
	buttons_box.add_theme_constant_override("separation",6)
	bottom.add_child(buttons_box)
	for id in ["move","aim","predict","fire","trap"]:
		var names={"move":"Laufen","aim":"Zielen","predict":"Tipp","fire":"Schuss","trap":"Fangfeld"}
		mode_buttons[id]=button(names[id],id,buttons_box,select_mode.bind(id))
	var row=HBoxContainer.new()
	bottom.add_child(row)
	button("Hinweis","hint",row,use_hint)
	button("Erklären","sound",row,replay_intro)
	button("Ausrüstung","gear",row,show_gear)
	menu_panel = PanelContainer.new()
	menu_panel.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	menu_panel.offset_left=-285;menu_panel.offset_right=285;menu_panel.offset_top=-260;menu_panel.offset_bottom=240
	menu_panel.add_theme_stylebox_override("panel",style(Color("152c42"),28))
	root.add_child(menu_panel)
	popup = PanelContainer.new()
	popup.set_anchors_and_offsets_preset(Control.PRESET_CENTER)
	popup.offset_left=-275;popup.offset_right=275;popup.offset_top=-260;popup.offset_bottom=250
	popup.add_theme_stylebox_override("panel",style(Color("19364a"),26))
	root.add_child(popup)
	popup.hide()
	voice = Voice.new()
	add_child(voice)
	update_score()

func show_menu():
	popup.hide()
	for child in menu_panel.get_children(): child.queue_free()
	var list=VBoxContainer.new()
	list.add_theme_constant_override("separation",18)
	menu_panel.add_child(list)
	list.add_child(label("ENERGYBLAST",36))
	list.add_child(label("Beobachten. Planen. Handeln.",23))
	for i in range(2):
		var info=definition.missions[i]
		var suffix="  + 2 Hinweise" if not progress.earned.has("mission:"+info.id) else "  ✓"
		button(info.title+suffix,"bank" if i==0 else "guardian",list,start_mission.bind(i)).custom_minimum_size.y=120
	button("Zurück zum Spiel","move",list,func(): menu_panel.hide())
	menu_panel.show()

func start_mission(index: int):
	menu_panel.hide()
	popup.hide()
	load_mission(index)
	replay_intro()

func replay_intro():
	voice.begin_mission("intro_"+mission.id, "gate" if mission.id=="guardian" else "move")

func all_walls() -> Array:
	var result=walls.duplicate()
	if mission.has("gate_rect") and not Geometry.gate_open(clock,definition.gate):
		result.append({"rect":rect(mission.gate_rect),"kind":"gate"})
	return result

func rect(values) -> Rect2:
	return Rect2(values[0],values[1],values[2],values[3])

func load_mission(index: int):
	mission=definition.missions[index].duplicate(true)
	player_pos=Geometry.v(mission.spawn)
	guardian_index=0;clock=0;awareness=0;detected_count=0;guard_frozen=0
	route=PackedVector2Array();prediction=null;trap_pos=null;trap_used=false;trap_life=0
	shots=0;complete=false;mission_solved=false;retry_left=0;trace_left=0;last_trace=[];shot_pending=false;pending_win=false
	mode="move";clue_visible=0
	if world != null: remove_child(world);world.queue_free()
	world=Node3D.new();add_child(world)
	box(world,Vector3(0,-.25,0),Vector3(14.2,.45,10.2),Color("284c59"))
	for x in range(-6,7):
		for z in range(-4,5): box(world,Vector3(x,-.017,z),Vector3(.025,.01,.025),Color("5a7f86"))
	walls=[]
	for values in [[-7,-5,14,.3],[-7,4.7,14,.3],[-7,-5,.3,10],[6.7,-5,.3,10]]:
		walls.append({"rect":rect(values),"kind":"border"})
		make_wall(values,Color("365a68"),.5)
	for values in mission.covers:
		walls.append({"rect":rect(values),"kind":"cover"})
		make_wall(values,Color("426e8c"),1.35)
	for values in mission.reflectors:
		walls.append({"rect":rect(values),"kind":"reflector"})
		make_wall(values,Color("55e5db"),1.1)
	player=load("res://assets/robot.glb").instantiate()
	world.add_child(player)
	player.position=Vector3(player_pos.x,0,player_pos.y)
	goal=Node3D.new();world.add_child(goal)
	goal.position=Vector3(mission.goal[0],.15,mission.goal[1])
	box(goal,Vector3(0,.25,0),Vector3(.85,.5,.85),Color("ffc75e"))
	sphere(goal,Vector3(0,.85,0),.27,Color("8bfff1"))
	secret=Node3D.new();world.add_child(secret)
	secret.position=Vector3(mission.secret.position[0],0,mission.secret.position[1])
	box(secret,Vector3(0,.3,0),Vector3(.65,.5,.5),Color("bd88f6"))
	box(secret,Vector3(0,.61,0),Vector3(.72,.12,.57),Color("ffd76a"))
	secret.hide()
	trap_node=Node3D.new();world.add_child(trap_node);trap_node.hide()
	for a in range(12):sphere(trap_node,Vector3(sin(a*TAU/12)*.95,.04,cos(a*TAU/12)*.95),.06,Color("a2f2cf"))
	gate_lights=[]
	if mission.id == "guardian":
		guardian_pos=Geometry.v(mission.patrol[0])
		guardian_forward=(Geometry.v(mission.patrol[1])-guardian_pos).normalized()
		guardian=load("res://assets/robot.glb").instantiate()
		guardian.scale=Vector3.ONE*1.35
		for node in guardian.find_children("*", "MeshInstance3D", true, false):
			if node.name.begins_with("Body") or node.name.begins_with("Arm") or node.name.begins_with("Boot"):
				node.material_override=material(Color("e8a758"))
		world.add_child(guardian)
		cone=MeshInstance3D.new();world.add_child(cone)
		cone.material_override=material(Color(.98,.64,.26,.35),true)
		cone.material_override.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
		cone.material_override.cull_mode=BaseMaterial3D.CULL_DISABLED
		var gr=rect(mission.gate_rect)
		gate=box(world,Vector3(gr.get_center().x,.6,gr.get_center().y),Vector3(gr.size.x,1.2,gr.size.y),Color("ce968e"))
		for x in range(3):gate_lights.append(sphere(world,Vector3(4.2+x*.6,1.8,-1),.16,Color("63798c")))
	else:
		guardian=null;gate=null;cone=null
	set_status("Tippe auf den Boden.")
	mode_buttons.trap.disabled = mission.id != "guardian"
	update_score()

func make_wall(values, color: Color, height: float):
	var r=rect(values)
	box(world,Vector3(r.get_center().x,height*.5,r.get_center().y),Vector3(r.size.x,height,r.size.y),color)

func set_status(text: String):
	status_label.text=text

func update_score():
	if is_instance_valid(player):
		for node in player.find_children("*", "MeshInstance3D", true, false):
			var m = node.material_override
			if m == null:
				m = node.get_active_material(0).duplicate()
				node.material_override = m
			if m is StandardMaterial3D:
				m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
				m.albedo_color.a = 1.0 - float(progress.stats().cloak) * 1.4
		if progress.total()>=160 and player.get_node_or_null("Shield") == null:
			var shield=box(player,Vector3(0,.95,.29),Vector3(.54,.32,.1),Color("ffd477"))
			shield.name="Shield"
	stars_label.text="★ " + str(progress.total())
	stars_label.add_theme_color_override("font_color",Color("ffdb79"))
	hints_label.text="? " + str(progress.hint_count())
	var tween=create_tween()
	stars_label.pivot_offset=stars_label.size*.5
	tween.tween_property(stars_label,"scale",Vector2.ONE*1.08,.12)
	tween.tween_property(stars_label,"scale",Vector2.ONE,.18)
	if not progress.save_ok: set_status("Speichern nicht möglich. Bitte Speicher prüfen.")

func select_mode(id: String):
	if complete: return
	if id=="fire": shoot();return
	mode=id
	if id in ["aim","predict","trap"]: route=PackedVector2Array()
	for key in mode_buttons:mode_buttons[key].tint=Color("ffdb79") if key==mode else Color("57ead1");mode_buttons[key].queue_redraw()
	voice.say(id)
	set_status({"move":"Tippe auf deinen Weg.","aim":"Tippe auf die leuchtende Wand.","predict":"Wo kommt der Schuss an? Setze deinen Tipp.","trap":"Tippe auf einen Platz für dein Fangfeld."}.get(id,""))

func _unhandled_input(event):
	if menu_panel.visible or popup.visible: return
	if event is InputEventScreenTouch and event.pressed: touch_world(event.position)
	elif event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT and event.pressed: touch_world(event.position)

func touch_world(screen: Vector2):
	if complete or retry_left>0: return
	var ray_origin=camera.project_ray_origin(screen)
	var direction=camera.project_ray_normal(screen)
	if absf(direction.y)<.00001:return
	var hit=ray_origin+direction*(-ray_origin.y/direction.y)
	var point=Vector2(clampf(hit.x,-6.4,6.4),clampf(hit.z,-4.3,4.3))
	match mode:
		"move": navigate(point)
		"aim":
			if point.distance_to(player_pos)>.4: aim=(point-player_pos).normalized()
		"predict": prediction=point
		"trap":
			if not trap_used and point.distance_to(player_pos)<3.5 and not blocked(point) and Geometry.cast(player_pos,(point-player_pos).normalized(),player_pos.distance_to(point),all_walls()).is_empty():
				trap_pos=point;trap_life=12;trap_used=true;trap_node.position=Vector3(point.x,0,point.y);trap_node.show();mode="move"

func blocked(point: Vector2) -> bool:
	if not Rect2(-6.5,-4.5,13,9).has_point(point):return true
	for wall in all_walls():
		if wall.rect.grow(.28).has_point(point):return true
	return false

func navigate(point: Vector2):
	var grid=AStarGrid2D.new()
	grid.region=Rect2i(0,0,36,26)
	grid.cell_size=Vector2.ONE*.4
	grid.offset=Vector2(-6.8,-4.8)
	grid.diagonal_mode=AStarGrid2D.DIAGONAL_MODE_ONLY_IF_NO_OBSTACLES
	grid.update()
	for x in range(36):
		for y in range(26):
			var cell=Vector2i(x,y)
			grid.set_point_solid(cell,blocked(grid.get_point_position(cell)))
	var start=Vector2i(((player_pos-grid.offset)/.4).round()).clamp(Vector2i.ZERO,Vector2i(35,25))
	var finish=Vector2i(((point-grid.offset)/.4).round()).clamp(Vector2i.ZERO,Vector2i(35,25))
	if grid.is_point_solid(finish):
		var best=100.0
		for x in range(36):
			for y in range(26):
				var cell=Vector2i(x,y)
				if grid.is_point_solid(cell):continue
				var d=grid.get_point_position(cell).distance_squared_to(point)
				if d<best:best=d;finish=cell
	grid.set_point_solid(start,false)
	route=grid.get_point_path(start,finish)
	if route.is_empty() and mission.has("gate_rect"):
		voice.say("gate_closed")
		if point.y< -1:navigate(Geometry.v(mission.staging))

func shot_preview() -> Dictionary:
	return Geometry.trace(player_pos+aim*.35,aim,all_walls(),int(progress.stats().bounces))

func shoot():
	if menu_panel.visible or popup.visible or complete or shot_pending:return
	if mission.id=="bank" and prediction==null:
		select_mode("predict")
		return
	var path=shot_preview()
	last_trace=path.points
	trace_left=2.2;shot_pending=true;pending_win=false;pending_skill=false;shots+=1
	if mission.id=="bank":
		for i in range(1,last_trace.size()-1):
			if Geometry.segment_distance(Geometry.v(mission.goal),last_trace[i],last_trace[i+1])<(.7 if progress.stats().lens else .6):
				pending_win=true
				pending_skill=prediction.distance_to(Geometry.v(mission.goal))<1.0
				last_trace.resize(i+2);last_trace[i+1]=Geometry.v(mission.goal)
				break
	else:
		for i in range(last_trace.size()-1):
			if Geometry.segment_distance(guardian_pos,last_trace[i],last_trace[i+1])<.7:guard_frozen=maxf(guard_frozen,.5)
	player.rotation.y=atan2(aim.x,aim.y)

func use_hint():
	if clue_cooldown>0:return
	clue_cooldown=1.2
	if progress.clue_level(mission.id)>=2:
		clue_visible=8
	elif progress.buy_clue(mission.id):
		clue_visible=8
	else:
		voice.say("hints_empty")
		set_status("Mission geschafft → zwei Hinweise. Die Erklärung bleibt kostenlos.")
		return
	voice.say("hint_"+mission.id)
	update_score()

func show_gear():
	for child in popup.get_children():child.queue_free()
	var list=VBoxContainer.new();popup.add_child(list)
	list.add_child(label("Deine Ausrüstung",30))
	for item in definition.unlocks:
		var names={"prism":"Prisma · zwei Abpraller", "armor":"Rüstung · mehr Reaktionszeit", "boots":"Stiefel · schneller laufen", "cloak":"Tarnung · schwerer zu entdecken"}
		var unlocked=progress.total()>=int(item.stars)
		var text=("✓ " if unlocked else str(int(item.stars))+" ★ ")+names[item.id]
		var gear_button=button(text,item.id,list,func():
			if item.id=="prism":progress.weapon="pulse" if progress.weapon=="prism" else "prism";progress.save()
			voice.say("upgrade"))
		gear_button.disabled=not unlocked
	list.add_child(label("Geheimfunde: "+str(int(progress.earned.has("secret:bank"))+int(progress.earned.has("secret:guardian")))+" / 2",22))
	button("Weiter","play",list,func():popup.hide())
	popup.show()

func _process(delta):
	if not is_instance_valid(player):return
	overlay.queue_redraw()
	if menu_panel.visible or popup.visible or backgrounded:return
	clock+=delta
	trace_left=maxf(0,trace_left-delta);clue_visible=maxf(0,clue_visible-delta);clue_cooldown=maxf(0,clue_cooldown-delta)
	if shot_pending and trace_left<1.45:
		shot_pending=false
		if pending_win:finish_mission(pending_skill)
		elif mission.id=="bank":voice.say("again")
	if complete:return
	if retry_left>0:
		retry_left-=delta
		if retry_left<=0:player_pos=Geometry.v(mission.spawn);awareness=0;route=PackedVector2Array();trap_used=false;trap_pos=null;trap_node.hide()
	else:
		if route.size()>0:
			var next=player_pos.move_toward(route[0],float(progress.stats().speed)*delta)
			if not blocked(next):
				var d=next-player_pos
				if d.length()>.0001:player.rotation.y=lerp_angle(player.rotation.y,atan2(d.x,d.y),minf(1,delta*12))
				player_pos=next
			else:route=PackedVector2Array()
			if route.size()>0 and player_pos.distance_to(route[0])<.04:route.remove_at(0)
	player.position=Vector3(player_pos.x,0,player_pos.y)
	animate_robot(player,clock,route.size()>0)
	if mission.id=="guardian":tick_guardian(delta)
	var sp=Geometry.v(mission.secret.position)
	var near=player_pos.distance_to(sp)<2.0
	var clear=Geometry.cast(player_pos,(sp-player_pos).normalized(),maxf(.001,player_pos.distance_to(sp)-.05),walls).is_empty()
	secret.visible=not progress.earned.has("secret:"+mission.id) and near and clear
	secret.rotation.y=clock*.4
	if secret.visible and player_pos.distance_to(sp)<.7:
		progress.award("secret:"+mission.id)
		voice.say("found");secret.hide();update_score()
	goal.rotation.y=clock*.3

func animate_robot(robot: Node3D, time: float, moving: bool):
	var wave=sin(time*11)*(.55 if moving else .045)
	robot.position.y = absf(sin(time*11))*.035 if moving else 0.0
	for name in ["Leg_L","Arm_R","Boot_L"]:
		var node=robot.find_child(name,true,false)
		if node:node.rotation.x=wave
	for name in ["Leg_R","Arm_L","Boot_R"]:
		var node=robot.find_child(name,true,false)
		if node:node.rotation.x=-wave

func tick_guardian(delta: float):
	guard_frozen=maxf(0,guard_frozen-delta)
	if guard_frozen<=0:
		var target=Geometry.v(mission.patrol[(guardian_index+1)%mission.patrol.size()])
		guardian_forward=(target-guardian_pos).normalized()
		guardian_pos=guardian_pos.move_toward(target,float(definition.guardian.speed)*delta)
		if guardian_pos.distance_to(target)<.06:guardian_index=(guardian_index+1)%mission.patrol.size()
	guardian.position=Vector3(guardian_pos.x,0,guardian_pos.y)
	guardian.rotation.y=atan2(guardian_forward.x,guardian_forward.y)
	animate_robot(guardian,clock,guard_frozen<=0)
	if trap_pos!=null:
		trap_life-=delta
		if trap_life<=0:trap_pos=null;trap_node.hide()
		elif guardian_pos.distance_to(trap_pos)<1.05:guard_frozen=3.5;trap_pos=null;trap_node.hide()
	var distance=float(definition.guardian.range)*(1.0-float(progress.stats().cloak))*(.9 if progress.stats().quiet else 1.0)
	var seen=Geometry.visible(guardian_pos,guardian_forward,player_pos,distance,float(definition.guardian.fov_degrees),walls) and guard_frozen<=0
	awareness=clampf(awareness+(delta if seen else -delta*2),0,2)
	if awareness>=float(progress.stats().grace) and retry_left<=0:
		detected_count+=1;retry_left=.9;route=PackedVector2Array();voice.say("seen");set_status("Deckung schützt dich. Du kannst gleich neu planen.")
	draw_cone(distance)
	var opened=Geometry.gate_open(clock,definition.gate)
	gate.scale.y=.12 if opened else 1.0
	var phase=fposmod(clock,float(definition.gate.period))
	for i in range(3):
		gate_lights[i].material_override=material(Color("68f6c6") if opened or phase>=3.0+i else Color("3b596d"),true)
	if opened and player_pos.distance_to(Geometry.v(mission.goal))<.8:finish_mission(detected_count==0)
	elif player_pos.y< -1.4 and player_pos.distance_to(Geometry.v(mission.goal))<.8:finish_mission(detected_count==0)

func draw_cone(distance: float):
	var vertices=PackedVector3Array()
	var forward_angle=atan2(guardian_forward.y,guardian_forward.x)
	for i in range(40):
		var a=forward_angle+deg_to_rad(-35+i*70.0/40)
		var b=forward_angle+deg_to_rad(-35+(i+1)*70.0/40)
		var pts=[]
		for angle in [a,b]:
			var d=Vector2(cos(angle),sin(angle))
			var hit=Geometry.cast(guardian_pos,d,distance,walls)
			pts.append(hit.point if not hit.is_empty() else guardian_pos+d*distance)
		vertices.append(Vector3(guardian_pos.x,.025,guardian_pos.y))
		vertices.append(Vector3(pts[1].x,.025,pts[1].y))
		vertices.append(Vector3(pts[0].x,.025,pts[0].y))
	var arr=[];arr.resize(Mesh.ARRAY_MAX);arr[Mesh.ARRAY_VERTEX]=vertices
	var mesh=ArrayMesh.new();mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arr);cone.mesh=mesh

func finish_mission(skill: bool):
	if complete or mission_solved:return
	complete=true;mission_solved=true;route=PackedVector2Array()
	var reward=progress.award("mission:"+mission.id)
	if skill:reward+=progress.award("skill:"+mission.id)
	update_score();voice.say("success")
	for child in popup.get_children():child.queue_free()
	var list=VBoxContainer.new();popup.add_child(list)
	list.add_child(label("Geschafft!",36));list.add_child(label("+ "+str(reward)+" ★     Gesamt: "+str(progress.total()),28))
	list.add_child(label("Neue Hinweise: "+str(progress.hint_count()),24))
	button("Geheimnisse suchen","hint",list,func():popup.hide();complete=false;clue_visible=0)
	button("Nächste Karte","play",list,func():show_menu())
	button("Noch einmal","play",list,func():start_mission(0 if mission.id=="bank" else 1))
	popup.show()

func _notification(what):
	if what == NOTIFICATION_APPLICATION_PAUSED:
		backgrounded=true
		if has_method("cancel_controls"):call("cancel_controls")
		if is_instance_valid(voice):voice.stream_paused=true
	elif what == NOTIFICATION_APPLICATION_RESUMED:
		backgrounded=false
		if is_instance_valid(voice):voice.stream_paused=false
	elif what == NOTIFICATION_WM_GO_BACK_REQUEST and is_instance_valid(menu_panel):
		show_menu()
