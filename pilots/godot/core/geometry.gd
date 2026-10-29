class_name PilotGeometry
extends RefCounted

static func v(value) -> Vector2:
	return Vector2(float(value[0]), float(value[1]))

static func cast(origin: Vector2, direction: Vector2, distance: float, walls: Array) -> Dictionary:
	var closest = distance + 0.001
	var result = {}
	for wall in walls:
		var r: Rect2 = wall.rect
		var sides = [[r.position.x, 0, Vector2.LEFT], [r.end.x, 0, Vector2.RIGHT], [r.position.y, 1, Vector2.UP], [r.end.y, 1, Vector2.DOWN]]
		for side in sides:
			var axis: int = side[1]
			if absf(direction[axis]) < 0.00001: continue
			var t = (side[0] - origin[axis]) / direction[axis]
			if t < 0.001 or t >= closest: continue
			var p = origin + direction * t
			var other = 1 - axis
			if p[other] < r.position[other] - 0.0001 or p[other] > r.end[other] + 0.0001: continue
			closest = t
			result = {"point": p, "normal": side[2], "kind": wall.kind, "distance": t}
	return result

static func trace(origin: Vector2, direction: Vector2, walls: Array, max_bounces: int = 1, length: float = 28.0) -> Dictionary:
	var points = [origin]
	var heading = direction.normalized()
	var cursor = origin
	var bounces = 0
	for _i in range(max_bounces + 2):
		var hit = cast(cursor, heading, length, walls)
		if hit.is_empty():
			points.append(cursor + heading * length)
			break
		points.append(hit.point)
		length -= hit.distance
		if hit.kind != "reflector" or bounces >= max_bounces: break
		bounces += 1
		heading = heading.bounce(hit.normal)
		cursor = hit.point + heading * 0.003
	return {"points": points, "bounces": bounces}

static func segment_distance(point: Vector2, a: Vector2, b: Vector2) -> float:
	return point.distance_to(Geometry2D.get_closest_point_to_segment(point, a, b))

static func visible(origin: Vector2, forward: Vector2, target: Vector2, distance: float, fov: float, walls: Array) -> bool:
	var delta = target - origin
	if delta.length() > distance: return false
	if delta.length() > 0.01 and forward.normalized().dot(delta.normalized()) < cos(deg_to_rad(fov * 0.5)): return false
	return cast(origin, delta.normalized(), delta.length() - 0.02, walls).is_empty()

static func gate_open(clock: float, config: Dictionary) -> bool:
	return fposmod(clock, float(config.period)) >= float(config.period) - float(config.open_seconds)
