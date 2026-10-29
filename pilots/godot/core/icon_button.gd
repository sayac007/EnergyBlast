extends Button
var icon_id = "move"
var tint = Color("57ead1")
func _ready():
	custom_minimum_size = Vector2(92, 86)
	add_theme_font_size_override("font_size", 16)
	resized.connect(queue_redraw)
func _draw():
	var c = Vector2(size.x * .5, 29)
	var color = tint if not disabled else Color("718697")
	match icon_id:
		"move", "boots":
			draw_circle(c + Vector2(-8, -7), 6, color)
			draw_circle(c + Vector2(8, 6), 6, color)
			draw_line(c + Vector2(-8, -1), c + Vector2(-8, 9), color, 7)
			draw_line(c + Vector2(8, 12), c + Vector2(8, 19), color, 7)
		"aim", "predict":
			draw_arc(c, 14, 0, TAU, 32, color, 3)
			for dir in [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN]: draw_line(c + dir * 9, c + dir * 21, color, 3)
			if icon_id == "predict": draw_circle(c, 4, Color("ffd66b"))
		"fire":
			draw_colored_polygon(PackedVector2Array([c + Vector2(4,-23), c + Vector2(-15,3), c + Vector2(-2,3), c + Vector2(-6,23), c + Vector2(16,-4), c + Vector2(3,-4)]), color)
		"trap":
			draw_arc(c, 19, 0, TAU, 32, color, 3)
			draw_arc(c, 10, 0, TAU, 24, color, 3)
		"hint":
			draw_arc(c + Vector2(0,-5), 12, -.3, PI + .3, 25, color, 4)
			draw_line(c + Vector2(-11,-1), c + Vector2(-5,12), color, 3)
			draw_line(c + Vector2(11,-1), c + Vector2(5,12), color, 3)
			draw_line(c + Vector2(-6,16), c + Vector2(6,16), color, 4)
		"gear", "armor":
			draw_colored_polygon(PackedVector2Array([c+Vector2(-17,-17),c+Vector2(17,-17),c+Vector2(15,6),c+Vector2(0,23),c+Vector2(-15,6)]), color)
		"bank", "prism":
			draw_line(c+Vector2(-23,-16),c+Vector2(23,-16),color,5)
			draw_polyline(PackedVector2Array([c+Vector2(-17,20),c+Vector2(0,-12),c+Vector2(20,16)]),color,4,true)
		"guardian":
			draw_style_box(get_theme_stylebox("normal"),Rect2(c-Vector2(22,20),Vector2(44,40)))
			draw_rect(Rect2(c-Vector2(17,14),Vector2(34,28)),color,false,3)
			draw_circle(c+Vector2(-7,-2),4,color)
			draw_circle(c+Vector2(7,-2),4,color)
		"cloak":
			draw_colored_polygon(PackedVector2Array([c+Vector2(0,-21),c+Vector2(-22,20),c+Vector2(22,20)]),Color(color,.45))
			draw_arc(c+Vector2(0,-8),8,PI,TAU,20,color,3)
		"play":
			draw_colored_polygon(PackedVector2Array([c+Vector2(-10,-19),c+Vector2(20,0),c+Vector2(-10,19)]),color)
		"sound":
			draw_colored_polygon(PackedVector2Array([c+Vector2(-17,-7),c+Vector2(-7,-7),c+Vector2(6,-19),c+Vector2(6,19),c+Vector2(-7,7),c+Vector2(-17,7)]),color)
			draw_arc(c+Vector2(5,0),19,-1.0,1.0,20,color,3)
