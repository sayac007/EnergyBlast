class_name PilotVoice
extends AudioStreamPlayer
var clips = {}
var waiting = ""
var important = []
var enabled = true
func _ready():
	var data = JSON.parse_string(FileAccess.get_file_as_string("res://assets/audio/de/manifest.json"))
	for row in data.clips: clips[row.id] = row
	finished.connect(_next)
func say(id: String):
	if not enabled or not clips.has(id): return
	if playing:
		if id in ["success", "found", "upgrade"]:
			if id not in important: important.append(id)
		else: waiting = id
		return
	var row = clips[id]
	stream = load("res://assets/audio/de/" + row.file)
	volume_db = float(row.playback_gain_db) - 1.0
	play()
func begin_mission(id: String, next: String):
	stop()
	important.clear()
	waiting=""
	say(id)
	important.append(next)
func _next():
	if not important.is_empty():
		say(important.pop_front())
		return
	if waiting != "":
		var next = waiting
		waiting = ""
		say(next)
func toggle():
	enabled = not enabled
	if not enabled:
		end_all()
func end_all():
	waiting=""
	important.clear()
	stop()
	stream=null
func _exit_tree():
	end_all()
