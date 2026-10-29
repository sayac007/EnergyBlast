extends Control
var game
func p(v: Vector2, height: float = .08) -> Vector2:
	return game.camera.unproject_position(Vector3(v.x, height, v.y))
func _draw():
	if game == null: return
	var c = Color("6bf4db")
	for v in game.route:
		draw_circle(p(v), 3, Color(c,.5))
	if game.mode in ["aim", "predict"] and not game.menu_panel.visible:
		var path = game.shot_preview()
		if path.points.size() >= 2:
			draw_line(p(game.player_pos),p(path.points[1]), Color(c,.65),3,true)
	if game.prediction != null:
		draw_arc(p(game.prediction),15,0,TAU,30,Color("eeb9ff"),3,true)
		draw_circle(p(game.prediction),3,Color("eeb9ff"))
	if game.trace_left > 0:
		for i in range(game.last_trace.size()-1):
			draw_line(p(game.last_trace[i],.18),p(game.last_trace[i+1],.18),Color(1,.82,.32,minf(1,game.trace_left)),5,true)
	if game.clue_visible > 0:
		var pos = PilotGeometry.v(game.mission.secret.hint_landmark)
		if game.progress.clue_level(game.mission.id) >= 2: pos = PilotGeometry.v(game.mission.secret.position)
		draw_arc(p(pos), 22 + sin(game.clock*4)*4, 0, TAU, 40, Color("ffe390"),4,true)
		var from = p(game.player_pos)
		var to = p(pos)
		draw_dashed_line(from,to,Color(1,.9,.5,.7),3,10,true)
