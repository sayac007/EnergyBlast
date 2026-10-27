extends "res://main.gd"
# Active combat is deliberately separate from the archived geometric pilot.
var combat_index=0
var turrets=[]
var bullets=[]
var particles=[]
var hp=3
var max_hp=3
var invulnerable=0.0
var fire_cooldown=0.0
var dash_cooldown=0.0
var dash_left=0.0
var fire_held=false
var touch_start=Vector2.ZERO
var touch_current=Vector2.ZERO
var aiming=false
var pointer_down=false
var active_touch=-1
var damage_taken=0
var combat_over=false
var health_label: Label
var mission_label: Label
var combat_overlay: Control
var sfx: AudioStreamPlayer
var fire_button: Button
var dash_button: Button

func _ready():
	var ui_theme=Theme.new();ui_theme.default_font=load("res://assets/fonts/LilitaOne-Regular.ttf");ui_theme.default_font.fallbacks=[ThemeDB.fallback_font];get_tree().root.theme=ui_theme
	definition=JSON.parse_string(FileAccess.get_file_as_string("res://assets/combat.json"))
	progress=Progress.new(definition)
	setup_environment()
	camera.position=Vector3(18,24,0);camera.look_at(Vector3.ZERO)
	setup_ui();load_mission(0);show_menu()
	sfx=AudioStreamPlayer.new();add_child(sfx)

func fit_camera():
	if not is_instance_valid(camera):return
	var viewport=get_viewport().get_visible_rect().size
	camera.keep_aspect=Camera3D.KEEP_HEIGHT
	camera.size=maxf(16.8,11.7/(viewport.x/maxf(1,viewport.y)))

func setup_ui():
	var canvas=CanvasLayer.new();add_child(canvas)
	var ui=Control.new();ui.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT);ui.mouse_filter=Control.MOUSE_FILTER_IGNORE;canvas.add_child(ui)
	combat_overlay=load("res://core/combat_overlay.gd").new();combat_overlay.game=self;combat_overlay.mouse_filter=Control.MOUSE_FILTER_IGNORE;combat_overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT);ui.add_child(combat_overlay)
	var top=VBoxContainer.new();top.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE);top.offset_left=20;top.offset_right=-20;top.offset_top=20;ui.add_child(top)
	var row=HBoxContainer.new();top.add_child(row)
	stars_label=label("★ 0",32);stars_label.size_flags_horizontal=Control.SIZE_EXPAND_FILL;row.add_child(stars_label)
	for item in [["≡",show_menu],["♫",func():voice.toggle()]]:
		var b=Button.new();b.text=item[0];b.custom_minimum_size=Vector2(78,66);b.add_theme_font_size_override("font_size",30);b.add_theme_stylebox_override("normal",style(Color("20314b"),24));row.add_child(b);b.pressed.connect(item[1])
	var second=HBoxContainer.new();top.add_child(second)
	health_label=label("",27);health_label.size_flags_horizontal=Control.SIZE_EXPAND_FILL;health_label.add_theme_color_override("font_color",Color("ff6c8a"));second.add_child(health_label)
	hints_label=label("",24);second.add_child(hints_label)
	mission_label=label("",20);top.add_child(mission_label)
	var bottom=VBoxContainer.new();bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE);bottom.offset_left=22;bottom.offset_right=-22;bottom.offset_top=-200;bottom.offset_bottom=-16;ui.add_child(bottom)
	status_label=label("Tippen: laufen. Ziehen: zielen. Loslassen: Feuer.",21);status_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER;status_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;bottom.add_child(status_label)
	var actions=HBoxContainer.new();actions.add_theme_constant_override("separation",18);bottom.add_child(actions)
	dash_button=action_button("»  DASH",Color("1d5969"),actions);dash_button.pressed.connect(dash)
	fire_button=action_button("ϟ  FEUER",Color("d63969"),actions);fire_button.button_down.connect(func():fire_held=true;shoot());fire_button.button_up.connect(func():fire_held=false)
	var extras=HBoxContainer.new();bottom.add_child(extras)
	for item in [["? Hinweis",use_hint],["♫ Funk",replay_intro],["◇ Ausrüstung",show_gear]]:
		var b=action_button(item[0],Color("20314b"),extras);b.custom_minimum_size.y=54;b.add_theme_font_size_override("font_size",18);b.pressed.connect(item[1])
	menu_panel=panel(ui);popup=panel(ui);popup.hide()
	voice=Voice.new();add_child(voice)

func action_button(text: String,color: Color,parent:Node) -> Button:
	var b=Button.new();b.text=text;b.custom_minimum_size=Vector2(90,92);b.size_flags_horizontal=Control.SIZE_EXPAND_FILL;b.add_theme_font_size_override("font_size",25)
	b.add_theme_stylebox_override("normal",style(color,34));b.add_theme_stylebox_override("pressed",style(color.lightened(.2),34));parent.add_child(b);return b
func panel(parent:Node) -> PanelContainer:
	var p=PanelContainer.new();p.set_anchors_and_offsets_preset(Control.PRESET_CENTER);p.offset_left=-295;p.offset_right=295;p.offset_top=-280;p.offset_bottom=280;p.add_theme_stylebox_override("panel",style(Color("18253e"),32));parent.add_child(p);return p
func clear_panel(p:Node):
	for child in p.get_children():p.remove_child(child);child.queue_free()
func cancel_controls():
	fire_held=false;pointer_down=false;active_touch=-1;aiming=false

func show_menu():
	if not is_instance_valid(menu_panel):return
	cancel_controls();popup.hide();clear_panel(menu_panel)
	var list=VBoxContainer.new();list.add_theme_constant_override("separation",14);menu_panel.add_child(list)
	list.add_child(label("ENERGYBLAST",42));list.add_child(label("RICOCHET RAID · 02",20))
	for i in range(definition.missions.size()):
		var m=definition.missions[i]
		var b=action_button(("01   " if i==0 else "02   ")+m.title,Color("24526a") if i==0 else Color("69395f"),list);b.custom_minimum_size.y=115;b.pressed.connect(start_mission.bind(i))
	list.add_child(label("Deckung. Timing. Ein kluger Schuss.",22))
	action_button("▶  WEITER",Color("263b58"),list).pressed.connect(func():menu_panel.hide())
	menu_panel.show()
func replay_intro():
	voice.begin_mission("combat_"+mission.id,"combat_controls")
func load_mission(index:int):
	combat_index=index;mission=definition.missions[index].duplicate(true);clock=0;player_pos=Geometry.v(mission.spawn);route=PackedVector2Array();aim=Vector2(8.5,-11.9).normalized();damage_taken=0
	bullets=[];particles=[];turrets=[];fire_held=false;pointer_down=false;active_touch=-1;aiming=false;combat_over=false;complete=false;mission_solved=false;retry_left=0;invulnerable=0;fire_cooldown=0;dash_cooldown=0;dash_left=0;clue_visible=0;clue_cooldown=0
	max_hp=int(definition.player.hit_points)+(1 if progress.total()>=160 else 0);hp=max_hp
	if world!=null:remove_child(world);world.queue_free()
	world=Node3D.new();add_child(world)
	world.add_child(load("res://assets/shooter/"+mission.id+".glb").instantiate())
	walls=[]
	for values in [[-7,-5,14,.3],[-7,4.7,14,.3],[-7,-5,.3,10],[6.7,-5,.3,10]]:walls.append({"rect":rect(values),"kind":"border"})
	for values in mission.covers:walls.append({"rect":rect(values),"kind":"cover"})
	for values in mission.reflectors:walls.append({"rect":rect(values),"kind":"reflector"})
	player=load("res://assets/shooter/hero.glb").instantiate();world.add_child(player);player.position=Vector3(player_pos.x,0,player_pos.y)
	for entry in mission.turrets:
		var node=load("res://assets/shooter/cannon.glb").instantiate();world.add_child(node);var pos=Geometry.v(entry.position);node.position=Vector3(pos.x,0,pos.y)
		turrets.append({"node":node,"position":pos,"hp":int(definition.combat.turret_hp),"shield":entry.shield,"timer":float(entry.phase)+.7,"warning":0.0,"direction":Vector2.LEFT,"flash":0.0})
	secret=Node3D.new();world.add_child(secret);var sp=Geometry.v(mission.secret.position);secret.position=Vector3(sp.x,0,sp.y)
	box(secret,Vector3(0,.35,0),Vector3(.7,.5,.55),Color("965ce9"));box(secret,Vector3(0,.64,0),Vector3(.77,.15,.60),Color("ffd873"));secret.hide()
	goal=Node3D.new();world.add_child(goal);goal.position=Vector3(mission.goal[0],0,mission.goal[1])
	if mission.exit_required:sphere(goal,Vector3(0,.5,0),.35,Color("52f6d5"))
	gate=null;gate_lights=[]
	if mission.has("gate_rect"):
		var gr=rect(mission.gate_rect);gate=box(world,Vector3(gr.get_center().x,.5,gr.get_center().y),Vector3(gr.size.x,1,gr.size.y),Color("f3a36c"))
		for i in range(3):gate_lights.append(sphere(world,Vector3(4.2+i*.6,1.5,-1),.15,Color("43566a")))
	mission_label.text=mission.title;set_status("Tippen: laufen · Ziehen und loslassen: schießen");update_score()
func update_score():
	if not is_instance_valid(stars_label):return
	stars_label.text="★ "+str(progress.total());stars_label.add_theme_color_override("font_color",Color("ffd674"));hints_label.text="? "+str(progress.hint_count())
	if is_instance_valid(health_label):health_label.text="♥ ".repeat(maxi(0,hp))+"♡ ".repeat(maxi(0,max_hp-hp))
	var t=create_tween();t.tween_property(stars_label,"scale",Vector2(1.10,1.10),.1);t.tween_property(stars_label,"scale",Vector2.ONE,.18)
	if not progress.save_ok:set_status("Spielstand konnte nicht gespeichert werden.")
func screen_world(screen:Vector2)->Vector2:
	var origin=camera.project_ray_origin(screen);var direction=camera.project_ray_normal(screen);var hit=origin+direction*(-origin.y/direction.y)
	return Vector2(clampf(hit.x,-6.4,6.4),clampf(hit.z,-4.3,4.3))
func _unhandled_input(event):
	if menu_panel.visible or popup.visible or backgrounded:return
	if event is InputEventScreenTouch:
		if event.pressed and active_touch<0:active_touch=event.index;pointer_down=true;touch_start=event.position;touch_current=event.position;aiming=false
		elif not event.pressed and event.index==active_touch:release_pointer(event.position);active_touch=-1
	elif event is InputEventScreenDrag and event.index==active_touch:drag_pointer(event.position)
	elif event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT:
		if event.pressed:pointer_down=true;touch_start=event.position;touch_current=event.position;aiming=false
		else:release_pointer(event.position)
	elif event is InputEventMouseMotion and pointer_down:drag_pointer(event.position)
func drag_pointer(point:Vector2):
	if not pointer_down:return
	touch_current=point
	if point.distance_to(touch_start)>14:
		aiming=true;route=PackedVector2Array();var target=screen_world(point)
		if target.distance_to(player_pos)>.3:aim=(target-player_pos).normalized()
func release_pointer(point:Vector2):
	if not pointer_down:return
	pointer_down=false
	if aiming:shoot()
	else:
		var target=screen_world(point);var enemy=false
		for t in turrets:
			if t.hp>0 and target.distance_to(t.position)<.8:enemy=true
		var reflector=not Geometry.cast(player_pos,(target-player_pos).normalized(),player_pos.distance_to(target)+.2,walls).is_empty() and blocked(target)
		if enemy or reflector:aim=(target-player_pos).normalized();shoot()
		else:navigate(target)
	aiming=false
func shoot():
	if combat_over or fire_cooldown>0 or menu_panel.visible or popup.visible:return
	fire_cooldown=float(definition.combat.fire_cooldown);shots+=1
	var path=Geometry.trace(player_pos+aim*.45,aim,all_walls(),int(progress.stats().bounces));spawn_bullet(path.points,false)
	player.rotation.y=atan2(aim.x,aim.y);beep(740,.07,.12)
func spawn_bullet(points:Array,enemy:bool):
	if points.size()<2:return
	var node=sphere(world,Vector3(points[0].x,.75,points[0].y),.13 if enemy else .11,Color("ff5475") if enemy else Color("a1fff0"))
	bullets.append({"points":points,"segment":0,"position":points[0],"enemy":enemy,"node":node,"speed":float(definition.combat.enemy_bullet_speed if enemy else definition.combat.player_bullet_speed)})
func dash():
	if dash_cooldown>0 or combat_over or menu_panel.visible:return
	if route.is_empty():navigate(player_pos+aim*2)
	dash_left=float(definition.player.dash_seconds);dash_cooldown=float(definition.player.dash_cooldown);invulnerable=maxf(invulnerable,dash_left);beep(400,.08,.10)
func beep(hz:float,seconds:float,gain:float):
	if not is_instance_valid(sfx) or not voice.enabled:return
	var wav=AudioStreamWAV.new();wav.format=AudioStreamWAV.FORMAT_16_BITS;wav.mix_rate=22050
	var data=PackedByteArray();data.resize(int(seconds*22050)*2)
	for i in range(data.size()/2):data.encode_s16(i*2,int(sin(TAU*hz*i/22050)*gain*32000*(1.0-float(i)/(data.size()/2))))
	wav.data=data;sfx.stream=wav;sfx.play()
func spark(pos:Vector2,color:Color):
	for i in range(7):
		var n=sphere(world,Vector3(pos.x,.7,pos.y),.065,color);particles.append({"node":n,"velocity":Vector3(sin(i*TAU/7)*2,1.6,cos(i*TAU/7)*2),"life":.45})
func damage_player():
	if invulnerable>0 or combat_over:return
	hp-=1;damage_taken+=1;invulnerable=float(definition.combat.hit_invulnerability);spark(player_pos,Color("ff5d7e"));update_score();beep(130,.15,.16)
	if hp<=0:
		combat_over=true;route=PackedVector2Array();fire_held=false;voice.say("combat_retry");clear_panel(popup)
		var list=VBoxContainer.new();popup.add_child(list);list.add_child(label("ENERGIE LEER",36));list.add_child(label("Sterne bleiben erhalten.",22));action_button("↻  NEUER ANLAUF",Color("d63969"),list).pressed.connect(start_mission.bind(combat_index));action_button("≡  SEKTOREN",Color("263b58"),list).pressed.connect(show_menu);popup.show()
func hit_turret(t:Dictionary,bounces:int):
	if t.shield and bounces==0:spark(t.position,Color("b277ff"));set_status("SCHILD · Triff über die leuchtende Wand.");voice.say("combat_shield");return
	t.hp-=1;t.flash=.18;spark(t.position,Color("ffce6d"));beep(250,.1,.14)
	if t.hp<=0:t.node.hide();spark(t.position,Color("75fff0"));if_all_destroyed()
func if_all_destroyed():
	for t in turrets:
		if t.hp>0:return
	if not mission.exit_required:finish_combat()
	else:set_status("KANONEN AUS · Erreiche den Energiekern.")
func finish_combat():
	if mission_solved:return
	mission_solved=true;combat_over=true;route=PackedVector2Array();fire_held=false
	var earned=progress.award("mission:"+mission.id)
	if damage_taken==0:earned+=progress.award("skill:"+mission.id)
	update_score();voice.say("combat_win");clear_panel(popup)
	var list=VBoxContainer.new();popup.add_child(list);list.add_child(label("SEKTOR GESICHERT",35));list.add_child(label("+ "+str(earned)+" ★     GESAMT "+str(progress.total()),27))
	action_button("◇  BEUTE SUCHEN",Color("24526a"),list).pressed.connect(func():popup.hide();combat_over=false)
	action_button("▶  SEKTOREN",Color("d63969"),list).pressed.connect(show_menu)
	action_button("↻  NOCH EINMAL",Color("263b58"),list).pressed.connect(start_mission.bind(combat_index));popup.show()
func use_hint():
	if clue_cooldown>0:return
	clue_cooldown=1.2
	if progress.clue_level(mission.id)<2 and not progress.buy_clue(mission.id):voice.say("hints_empty");return
	clue_visible=8;voice.say("hint_bank" if mission.id=="reactor" else "hint_guardian");update_score()
func show_gear():
	cancel_controls()
	clear_panel(popup);var list=VBoxContainer.new();popup.add_child(list);list.add_child(label("ARSENAL",36))
	for row in [[100,"PRISMA · 2 ABPRALLER"],[160,"RÜSTUNG · +1 ENERGIE"],[230,"STIEFEL · MEHR TEMPO"],[300,"TARNUNG · KÜRZERE REICHWEITE"]]:list.add_child(label(("✓  " if progress.total()>=row[0] else str(row[0])+" ★  ")+row[1],21))
	action_button("WEITER",Color("24526a"),list).pressed.connect(func():popup.hide());popup.show()
func _process(delta):
	if not is_instance_valid(player):return
	combat_overlay.queue_redraw()
	if menu_panel.visible or popup.visible or backgrounded:return
	var dt=minf(delta,.05);clock+=dt;invulnerable=maxf(0,invulnerable-dt);fire_cooldown=maxf(0,fire_cooldown-dt);dash_left=maxf(0,dash_left-dt);dash_cooldown=maxf(0,dash_cooldown-dt);clue_visible=maxf(0,clue_visible-dt);clue_cooldown=maxf(0,clue_cooldown-dt)
	if combat_over:return
	if fire_held:shoot()
	if not route.is_empty():
		var speed=float(definition.player.speed)+float(progress.stats().speed)-3.0
		if dash_left>0:speed=float(definition.player.dash_speed)
		var next=player_pos.move_toward(route[0],speed*dt)
		if not blocked(next):
			var direction=next-player_pos
			if direction.length()>.001 and not fire_held and not aiming:player.rotation.y=lerp_angle(player.rotation.y,atan2(direction.x,direction.y),minf(1,dt*14))
			player_pos=next
		else:route=PackedVector2Array()
		if not route.is_empty() and player_pos.distance_to(route[0])<.04:route.remove_at(0)
	player.position=Vector3(player_pos.x,0,player_pos.y);animate_robot(player,clock,not route.is_empty());player.visible=invulnerable<=0 or fmod(clock,.13)>.05
	for t in turrets:
		if t.hp<=0:continue
		t.flash=maxf(0,t.flash-dt);t.node.scale=Vector3.ONE*(1.0+t.flash*.3)
		if t.warning>0:
			t.warning-=dt
			if t.warning<=0:
				var hit=Geometry.cast(t.position,t.direction,20,all_walls());var end=hit.point if not hit.is_empty() else t.position+t.direction*20
				spawn_bullet([t.position,end],true);t.timer=float(definition.combat.enemy_interval);beep(190,.08,.10)
		else:
			t.timer-=dt
			if t.timer<=0 and t.position.distance_to(player_pos)<13.0*(1.0-float(progress.stats().cloak)*.5)*(.9 if progress.stats().quiet else 1.0):t.warning=float(definition.combat.enemy_warning);t.direction=(player_pos-t.position).normalized()
		t.node.rotation.y=atan2(t.direction.x,t.direction.y)
	update_bullets(dt)
	for particle in particles.duplicate():
		particle.life-=dt;particle.node.position+=particle.velocity*dt;particle.velocity.y-=5*dt
		if particle.life<=0:particle.node.queue_free();particles.erase(particle)
	var sp=Geometry.v(mission.secret.position);var dist=player_pos.distance_to(sp)
	secret.visible=not progress.earned.has("secret:"+mission.id) and dist<2 and Geometry.cast(player_pos,(sp-player_pos).normalized(),maxf(.001,dist-.05),walls).is_empty()
	secret.rotation.y=clock*.5
	if secret.visible and dist<.7:progress.award("secret:"+mission.id);voice.say("combat_loot");update_score();secret.hide()
	if gate!=null:
		gate.scale.y=.10 if Geometry.gate_open(clock,definition.gate) else 1.0
		for i in range(3):gate_lights[i].material_override=material(Color("68f6c6") if fmod(clock,8)>=3+i else Color("35445b"),true)
	if mission.exit_required and player_pos.distance_to(Geometry.v(mission.goal))<.8:
		var alive=false
		for t in turrets:alive=alive or t.hp>0
		if not alive:finish_combat()
	dash_button.text="»  DASH" if dash_cooldown<=0 else "»  "+str(snappedf(dash_cooldown,.1))
func update_bullets(dt:float):
	for b in bullets.duplicate():
		var distance=b.speed*dt;var removed=false
		while distance>0 and b.segment<b.points.size()-1:
			var target=b.points[b.segment+1];var step=minf(distance,b.position.distance_to(target));var next:Vector2=b.position.move_toward(target,step)
			if b.enemy:
				if Geometry.segment_distance(player_pos,b.position,next)<.36:damage_player();removed=true
			else:
				for t in turrets:
					if t.hp>0 and Geometry.segment_distance(t.position,b.position,next)<(.56 if progress.stats().lens else .48):hit_turret(t,b.segment);removed=true;break
			b.position=next;distance-=step
			if removed:break
			if b.position.distance_to(target)<.001:
				b.segment+=1;spark(target,Color("84fff0") if not b.enemy else Color("ff9a72"))
				if b.segment<b.points.size()-1:beep(1000,.035,.08)
			if step<.00001:break
		b.node.position=Vector3(b.position.x,.75,b.position.y)
		if removed or b.segment>=b.points.size()-1:b.node.queue_free();bullets.erase(b)
