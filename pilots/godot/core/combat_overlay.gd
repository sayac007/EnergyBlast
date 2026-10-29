extends Control
var game
func point(v:Vector2,h:float=.12)->Vector2:return game.camera.unproject_position(Vector3(v.x,h,v.y))
func _draw():
	if game==null or not is_instance_valid(game.player):return
	for p in game.route:draw_circle(point(p),2,Color("6edbd2",.6))
	if game.aiming and not game.menu_panel.visible:
		var path=game.shot_preview()
		for i in range(path.points.size()-1):draw_dashed_line(point(path.points[i],.75),point(path.points[i+1],.75),Color("a7fff0",.85),2,9,true)
		draw_arc(point(game.screen_world(game.touch_current)),15,0,TAU,30,Color("ffe191"),3,true)
	for t in game.turrets:
		if t.hp<=0:continue
		var p=point(t.position,1.5)
		draw_style_box(bar(Color("11223b")),Rect2(p-Vector2(24,7),Vector2(48,7)))
		draw_style_box(bar(Color("ff6b85")),Rect2(p-Vector2(24,7),Vector2(24*t.hp,7)))
		if t.shield:draw_arc(point(t.position,.8),27,0,TAU,36,Color("bb8aff",.75),2,true)
		if t.warning>0:
			var hit=PilotGeometry.cast(t.position,t.direction,20,game.all_walls())
			var end=hit.point if not hit.is_empty() else t.position+t.direction*20
			draw_dashed_line(point(t.position,.75),point(end,.75),Color("ff6b85",.65),3,10,true)
			draw_arc(point(t.position,1.3),21,-PI/2,-PI/2+TAU*(1-t.warning/game.definition.combat.enemy_warning),24,Color("ffdc7e"),4,true)
	for b in game.bullets:
		var p=point(b.position,.75);draw_circle(p,8,Color("ff6485",.16) if b.enemy else Color("6effe7",.16));draw_circle(p,3,Color("ffe3b8") if b.enemy else Color("dcfff7"))
	if game.clue_visible>0:
		var target=PilotGeometry.v(game.mission.secret.position if game.progress.clue_level(game.mission.id)>1 else game.mission.secret.hint_landmark)
		draw_dashed_line(point(game.player_pos),point(target),Color("ffdb7d"),3,9,true);draw_arc(point(target),22,0,TAU,30,Color("ffdb7d"),3,true)
func bar(color:Color)->StyleBoxFlat:
	var b=StyleBoxFlat.new();b.bg_color=color;b.set_corner_radius_all(3);return b
