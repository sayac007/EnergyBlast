class_name PilotProgress
extends RefCounted

var data: Dictionary
var earned: Dictionary = {}
var clues: Array = []
var weapon = "pulse"
var path = "user://energyblast-progress.json"
var save_ok = true

func _init(definition: Dictionary, save_path: String = "user://energyblast-progress.json"):
	data = definition
	path = save_path
	load_saved()

func load_saved():
	for candidate in [path, path + ".bak"]:
		if not FileAccess.file_exists(candidate): continue
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(candidate))
		if not parsed is Dictionary or parsed.get("schema") != 1: continue
		if not parsed.get("earned") is Dictionary or not parsed.get("clues") is Array: continue
		earned.clear()
		for key in parsed.earned:
			if data.rewards.has(key) and parsed.earned[key] == true: earned[key] = true
		clues.clear()
		for id in parsed.clues:
			if id in valid_clue_ids() and id not in clues and clues.size() < earned_clue_count(): clues.append(id)
		weapon = "prism" if parsed.get("weapon") == "prism" and total() >= 100 else "pulse"
		return

func valid_clue_ids() -> Array:
	var result=[]
	for id in data.get("progress_mission_ids", ["bank", "guardian"]):
		result.append(id+":1");result.append(id+":2")
	return result

func total() -> int:
	var value = 0
	for key in earned: value += int(data.rewards.get(key, 0))
	return value

func earned_clue_count() -> int:
	var value = 0
	for key in data.get("hint_completion_keys", ["mission:bank", "mission:guardian"]):
		if earned.has(key): value += int(data.hint_reward_per_mission)
	return value

func hint_count() -> int:
	return earned_clue_count() - clues.size()

func award(id: String) -> int:
	if earned.has(id) or not data.rewards.has(id): return 0
	var before = total()
	earned[id] = true
	if before < 100 and total() >= 100: weapon = "prism"
	save()
	return total() - before

func clue_level(mission: String) -> int:
	return int((mission + ":1") in clues) + int((mission + ":2") in clues)

func buy_clue(mission: String) -> bool:
	if mission not in data.get("progress_mission_ids", ["bank", "guardian"]) or hint_count() <= 0 or clue_level(mission) >= 2: return false
	clues.append(mission + ":" + str(clue_level(mission) + 1))
	save()
	return true

func stats() -> Dictionary:
	var stars = total()
	return {"speed": 3.0 + (minf(.5, (stars - 220.0) / 210.0) if stars >= 230 else 0.0), "grace": 1.4 if stars >= 160 else 1.0, "cloak": minf(.35, (stars - 280.0) / 180.0) if stars >= 300 else 0.0, "bounces": 2 if weapon == "prism" and stars >= 100 else 1, "lens": earned.has("secret:bank") or earned.has("secret:reactor"), "quiet": earned.has("secret:guardian") or earned.has("secret:citadel")}

func save():
	var file = FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if file == null:
		save_ok = false
		return
	file.store_string(JSON.stringify({"schema": 1, "earned": earned, "clues": clues, "weapon": weapon}))
	file.flush()
	file.close()
	var absolute = ProjectSettings.globalize_path(path)
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(absolute + ".bak")
		DirAccess.rename_absolute(absolute, absolute + ".bak")
	save_ok = DirAccess.rename_absolute(absolute + ".tmp", absolute) == OK
