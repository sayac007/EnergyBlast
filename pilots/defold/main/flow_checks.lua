-- Regression for the formerly stranded post-win state and truthful navigation.
local Combat=require 'main.combat'
local M={}
function M.run(original)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function saved()return{earned={},clues={},weapon='pulse',schema=2,purchases={},spent={}}end
 local function fresh(index,store)
  local g=Combat.new(original.data,store or saved());g:load(index or 1)
  for _,enemy in ipairs(g.enemies)do enemy.warning=0;enemy.timer=999 end
  return g
 end
 local g=fresh()
 check(g:start_index()==1,'fresh campaign starts at first mission')
 for _,bad in ipairs({0,-1,1.5,999,'2',false})do
  local s=saved();s.current_mission=bad
  local restored=Combat.new(original.data,s)
  check(restored.index==1 and restored.saved.current_mission==1,'invalid saved mission recovers safely: '..tostring(bad))
 end
 local s=saved();s.current_mission=4;s.character='dragon';s.purchases.armor=true;s.spent.armor=160
 g=Combat.new(original.data,s)
 check(g.index==4 and g:start_index()==4,'validated mission survives construction')
 check(g:character().id=='dragon'and g:owns('armor')and g.saved.spent.armor==160,'navigation migration preserves character and purchases')
 check(not g:remember_mission(0)and g.saved.current_mission==4,'invalid navigation cannot overwrite saved selection')
 check(g:remember_mission(3)and g:start_index()==3,'explicit valid selection persists')
 local next_load=Combat.new(original.data,g.saved)
 check(next_load.index==3,'separate reconstruction restores selected mission')
 s=saved();s.earned['mission:'..original.data.missions[1].id]=true
 g=Combat.new(original.data,s)
 check(g.index==2 and not g.solved,'legacy completed mission chooses next but never auto-completes current round')
 s=saved();for _,mission in ipairs(original.data.missions)do s.earned['mission:'..mission.id]=true end
 g=Combat.new(original.data,s)
 check(g.index==#original.data.missions and g:next_index()==nil,'completed campaign never loads a non-existent successor')
 g=fresh(3);local state=g:mission_state()
 local enemies,relays=0,0
 for _,enemy in ipairs(g.enemies)do if not enemy.optional and enemy.hp>0 then if enemy.kind=='relay'then relays=relays+1 else enemies=enemies+1 end end end
 check(state.enemies==enemies and state.relays==relays,'counters exclude optional bonus entities')
 check(state.goal_kind=='relay','relay shields are explained before pointing at protected boss')
 for _,enemy in ipairs(g.enemies)do if not enemy.optional then enemy.hp=0 end end
 state=g:mission_state()
 check(state.goal_kind=='exit'and state.enemies==0 and state.relays==0,'defeated enemies switch guidance to required exit')
 g.clock=0;check(not g:mission_state().exit_open,'closed timing gate is reported truthfully')
 g.clock=5;check(g:mission_state().exit_open,'open timing gate is reported truthfully')
 g=fresh(5);state=g:mission_state()
 check(state.sequence_remaining==#g.m.sequence and state.goal_kind=='sequence','sequence has its own remaining-objective count')
 local expected=g.m.sequence_nodes[g.m.sequence[1]]
 check(math.abs(state.goal[1]-expected[1])>.01 or math.abs(state.goal[2]-expected[2])>.01,'compass indicates observation area, never correct next crystal')
 local observation=state.goal;g.sequence_progress=1;state=g:mission_state()
 check(state.goal[1]==observation[1]and state.goal[2]==observation[2],'sequence progress cannot turn compass into an answer hint')
 g=fresh();state=g:mission_state()
 check(state.treasures_remaining==1 and not state.primary_done,'one optional treasure is explicitly still available')
 local total,credits=g:total(),g:credits()
 check(g:track_treasure()and g:mission_state().goal_kind=='treasure','treasure can be tracked without buying a clue')
 check(g:total()==total and g:credits()==credits and not g.peaceful,'tracking neither spends currency nor disables combat')
 check(g:mission_state().goal[1]==g.m.secret.hint_landmark[1]and g:mission_state().goal[2]==g.m.secret.hint_landmark[2],'distant free guidance identifies landmark rather than silently revealing entire secret')
 g:track_objective();check(g:mission_state().goal_kind~='treasure','primary target can be restored without restarting')
 g.saved.earned['secret:'..g.m.id]=true
 check(g:mission_state().treasures_remaining==0 and not g:track_treasure(),'already collected treasure is never advertised as remaining')
 g=fresh();local last
 for _,enemy in ipairs(g.enemies)do if not enemy.optional then last=enemy;enemy.hp=0 end end
 last.hp=1;last.shield=false;g:hit(last,0)
 check(g.solved and g.bonus.completed==0,'actual final enemy hit completes mission while both bonuses remain optional')
 g=fresh(2);for _,enemy in ipairs(g.enemies)do if not enemy.optional then enemy.hp=0 end end
 g.p={g.m.goal[1],g.m.goal[2]};g.clock=5;g:update(.025)
 check(g.solved and g.bonus.completed==0,'actual exit crossing does not require destroying optional bonus targets')
 g=fresh();local mission=g.m.id
 g:finish();local rewarded=g:total();state=g:mission_state()
 check(g.solved and g.over and g.paused and state.primary_done and state.treasures_remaining==1,'victory is independent of optional treasure')
 check(g.saved.current_mission==2,'victory remembers next mission for next app start')
 g:finish();check(g:total()==rewarded,'opening victory twice never grants duplicate stars')
 local chosen=nil;g.choose=function(index)chosen=index end
 check(g:next_mission()and chosen==2,'next button requests actual successor even with treasure left')
 check(g:total()==rewarded,'advancing without treasure cannot invent its reward')
 g.dialog='gear';g:resume_mission()
 check(not g.paused and not g.over and g.solved and g.peaceful and g.dialog==nil,'continue after win cannot strand simulation behind over=true')
 check(g.pending_win==nil and g:open(),'peaceful search cannot reopen victory dialog or close access gates')
 local hp=g.hp;g.invulnerable=0;g:hit_player()
 check(g.hp==hp,'post-win search is safe from damage')
 g.bullets={};g:update(.05)
 check(#g.bullets==0,'peaceful search produces no hostile fire')
 check(g:search_loot()and g.navigation_focus=='treasure','optional search has its own explicit navigation mode')
 local sp=g.m.secret.position;g.p={sp[1],sp[2]};g:update(.05)
 check(g.saved.earned['secret:'..mission]and g:mission_state().treasures_remaining==0,'searching actually collects and removes remaining treasure')
 local with_treasure=g:total();g:update(.1);check(g:total()==with_treasure,'treasure collection is one-time during free exploration')
 check(g.bonus and #g.bonus.tasks==2 and g:mission_state().goal_kind=='bonus','remaining integrated bonuses are guided after treasure')
 g=fresh();check(not g:search_loot()and not g.peaceful,'search button cannot bypass an unfinished battle')
 g.paused=true;g.dialog='gear';g.p={-6,4};g.hp=2;local p=g.p
 g:resume_mission()
 check(not g.paused and not g.over and g.p==p and g.hp==2 and not g.peaceful,'resume during live mission retains position and damage')
 g.over=true;g.dialog='defeat';chosen=nil;g.choose=function(index)chosen=index end;g:resume_mission()
 check(chosen==g.index,'resume after defeat requests a real retry instead of reviving broken state')
 g=fresh(#original.data.missions);g:finish();chosen=nil;g.choose=function(index)chosen=index end
 check(not g:next_mission()and chosen==nil and g.dialog=='menu','last mission returns to campaign without invalid successor')
 return n
end
return M
