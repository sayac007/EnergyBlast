extends SceneTree
const P=preload("res://core/progress.gd")
func _initialize():
	var definition=JSON.parse_string(FileAccess.get_file_as_string("res://assets/pilot.json"))
	var progress=P.new(definition)
	if "--write" in OS.get_cmdline_user_args():
		assert(progress.total()==0)
		progress.award("mission:bank")
		progress.award("skill:bank")
		assert(progress.buy_clue("bank"))
		assert(progress.save_ok)
		print("PERSISTENCE WRITE PASS: 100 stars, one remaining clue")
	else:
		assert(progress.total()==100 and progress.hint_count()==1 and progress.clue_level("bank")==1)
		assert(progress.award("mission:bank")==0)
		assert(progress.stats().bounces==2)
		print("PERSISTENCE RESTART PASS: score, unlock, purchase, replay protection")
	quit()
