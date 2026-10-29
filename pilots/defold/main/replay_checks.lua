-- Earned rewards are permanent; optional challenges remain playable on revisits.
local Combat=require 'main.combat'
local Bonus=require 'main.bonus'
local Shots=require 'main.projectiles'
local M={}
local function store(data)
 local s={earned={},clues={'reactor:1'},schema=3,purchases={prism=true,armor=true},spent={prism=100,armor=160},weapon='prism',character='dragon',music=false,current_mission=1}
 for _,mission in ipairs(data.missions)do
  for _,prefix in ipairs({'mission:','skill:','secret:','bonus:prism:','bonus:pattern:'})do s.earned[prefix..mission.id]=true end
 end
 return s
end
function M.run(data)
 if not data.optional_replay then return 0 end
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(i,s)
  local g=Combat.new(data,s);g:load(i)
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil end
  g.invulnerable=999;return g
 end
 for index,mission in ipairs(data.missions)do
  local g=fresh(index,store(data));local before,wallet,credits=g:total(),g:wallet(),g:credits()
  local speech;g.say=function(id)speech=id end
  local state=g:mission_state();local treasure=g:treasure_state()
  check(state.bonus_done==0 and state.bonus_total==2,'earned save restores two unfinished round bonuses '..mission.id)
  check(state.bonus_rewarded==2 and state.bonus_replay==2,'UI distinguishes permanent rewards from round completion '..mission.id)
  check(treasure.available and treasure.reward_earned and treasure.replay and treasure.discovered,'earned chest is visible replay loot '..mission.id)
  check(state.treasures_remaining==1 and state.treasure_rewarded and state.treasure_replay,'chest round count and saved reward remain distinct '..mission.id)
  for _,task in ipairs(g.bonus.tasks)do
   check(not task.done and task.rewarded and task.replay,'every previously earned task rearms '..mission.id..task.id)
   for _,e in ipairs(task.targets)do
    check(e.hp==1 and not g:blocked(e.p),'replay target has live health on free floor '..mission.id)
    g:navigate(e.p);check(#g.path>0,'replay target is reachable from actual movement graph '..mission.id)
   end
  end
  g.path={};check(g:hint()and g.navigation_focus=='bonus'and speech=='bonus_prism','hint explains a real replay task instead of claiming map empty '..mission.id)
  check(g:credits()==credits,'replay guidance cannot spend a clue '..mission.id)
  g:track_objective();g:guide()
  check(speech=='bonus_prism'and g:mission_state().goal_kind=='bonus','Info restores useful bonus guidance from prior earned save '..mission.id)
  local prism=g.bonus.tasks[1];local crystal=prism.targets[1]
  g:hit(crystal,0);check(not prism.done and crystal.hp==1,'replay retains real bank-shot requirement '..mission.id)
  -- All six left-side crystals have a genuine reachable one-wall firing solution.
  -- Preserve the mission's real walls, absorbers and sanctuary during the shot.
  local firing={-9,crystal.p[2]};g:navigate(firing)
  check(not g:blocked(firing)and #g.path>0 and Combat.dist(g.path[#g.path],firing)<.4,'reachable real reflection vantage '..mission.id)
  local enemies=g.enemies;g.enemies={crystal};g.p=firing;g.path={};g.aim={-1,0};g.cooldown=0
  g:fire();for frame=1,160 do Shots.update(g,.025)end
  check(prism.done and crystal.hp==0 and g.bonus.completed==1,'actual reflected projectile completes replay crystal '..mission.id)
  check(g:total()==before and g:wallet()==wallet,'replayed bank shot cannot duplicate stars '..mission.id)
  g.enemies=enemies
  local pattern=g.bonus.tasks[2]
  if pattern.kind=='sequence'then
   for _,order in ipairs(pattern.sequence)do g:hit(pattern.targets[order],0)end
  else
   g:hit(pattern.targets[1],0)
   check(not pattern.done,'replayed timing task still rejects red shots '..mission.id)
   Bonus.update(g,3.01);g:hit(pattern.targets[1],0)
  end
  check(pattern.done and g.bonus.completed==2 and g:mission_state().bonus_done==2,'second replay challenge completes in current round '..mission.id)
  check(g:total()==before and g:wallet()==wallet,'all replay rewards remain one-time '..mission.id)
  g.solved=true;g:resume_mission();g:guide()
  check(g.bonus.completed==2 and speech=='flow_treasure','resume preserves round completion and points at remaining replay chest '..mission.id)
  local sp=mission.secret.position;g.p={sp[1],sp[2]};g:update_treasure()
  check(g.treasure_collected and not g:treasure_state().available and not g.secret_visible,'replay chest can really be collected once per visit '..mission.id)
  check(g:total()==before and g:wallet()==wallet and g:credits()==credits,'replay chest changes neither saved stars wallet nor clues '..mission.id)
  check(g.saved.purchases.prism and g.saved.purchases.armor and g.saved.spent.prism==100 and g.saved.spent.armor==160 and g.saved.weapon=='prism'and g.saved.character=='dragon'and g.saved.music==false,'old purchases weapon character and music survive replay '..mission.id)
  g:resume_mission();g:track_objective();g.hint_debounce=0;g:hint()
  check(not g:treasure_state().available and g.bonus.completed==2 and speech=='flow_no_treasure','fully collected current round is reported honestly '..mission.id)
  local restored=fresh(index,g.saved)
  check(restored.bonus.completed==0 and restored:treasure_state().available and restored:total()==before,'new visit rearms visuals without erasing reward ledger '..mission.id)
 end
 -- Fresh saves retain first-time rewards; reload adds gameplay without farming.
 local g=fresh(1);local crystal=g.bonus.tasks[1].targets[1]
 g:hit(crystal,1);check(g:total()==100 and not g.bonus.tasks[1].replay,'fresh first completion still pays advertised bonus')
 g:load(1);crystal=g.bonus.tasks[1].targets[1];g:hit(crystal,1)
 check(g:total()==100 and g.bonus.tasks[1].done and g.bonus.tasks[1].replay,'reloaded first reward remains playable without a second payment')
 return n
end
return M
