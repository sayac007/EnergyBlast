-- Current treasure guidance: a hint points to reachable ground and can be found.
local Combat=require 'main.combat'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function saved()return{earned={},clues={},weapon='pulse',schema=3,purchases={},spent={}}end
 local function fresh(index,store)
  local g=Combat.new(data,store or saved());g:load(index or 1)
  for _,enemy in ipairs(g.enemies)do enemy.warning=0;enemy.timer=999;enemy.patrol=nil end
  g.invulnerable=999;return g
 end
 local function step(g,seconds)
  for i=1,math.ceil(seconds/.025)do g:update(.025)end
 end
 local function path_length(g)
  local length=0;local p=g.p
  for _,point in ipairs(g.path)do length=length+Combat.dist(p,point);p=point end
  return length
 end
 for index,mission in ipairs(data.missions)do
  local g=fresh(index);local sp=mission.secret.position;local hint=mission.secret.hint_landmark
  check(not g:blocked(sp),'actual chest is on walkable ground '..mission.id)
  check(not g:blocked(hint),'search landmark is outside solid cover '..mission.id)
  g:navigate(hint)
  check(#g.path>0 and Combat.dist(g.path[#g.path],hint)<.4,'real path reaches search marker '..mission.id)
  g.path={};local credits=g:credits();local spoken
  g.say=function(id)spoken=id end
  check(g:hint()and g.navigation_focus=='treasure','hint switches compass from enemy to treasure '..mission.id)
  check(g:credits()==credits and #g.saved.clues==0,'zero-credit search guidance is free '..mission.id)
  check(spoken=='defold_treasure_hint','spoken and visible guidance share current treasure instruction '..mission.id)
  local state=g:treasure_state();check(state.available and state.tracking,'free guidance remains visible '..mission.id)
  local goal=g:mission_state();check(goal.goal_kind=='treasure'and not g:blocked(goal.goal),'compass never points inside cover '..mission.id)
  g:navigate(sp);local length=path_length(g)
  check(#g.path>0 and length<45,'real navigable route to chest exists '..mission.id)
  local before=g:total();step(g,length/data.player.speed+.6)
  check(g.saved.earned['secret:'..mission.id]==true,'actual walking collects chest '..mission.id)
  check(g:total()==before+data.rewards['secret:'..mission.id],'walking awards the advertised treasure once '..mission.id)
  check(not g:treasure_state().available and not g.secret_visible,'collected chest and marker vanish '..mission.id)
  g.hint_debounce=0;credits=g:credits();g:hint()
  check(g:credits()==credits and spoken=='flow_no_treasure','collected chest cannot consume another clue '..mission.id)
  local restored=fresh(index,g.saved)
  check(not restored:treasure_state().available,'collected chest stays removed after reload '..mission.id)
  before=g:total();step(g,.2);check(g:total()==before,'proximity cannot double-pay treasure '..mission.id)
  -- The increased radius is useful on a phone, without exact center taps.
  g=fresh(index);g.p={sp[1],sp[2]-.95};step(g,.05)
  check(g.saved.earned['secret:'..mission.id]==true,'95-centimeter approach collects without exact tap '..mission.id)
 end
 local g=fresh();local sp=g.m.secret.position
 check(not g:treasure_state().discovered,'distant fresh chest starts undiscovered')
 g.p={-6.75,-.8};local state=g:treasure_state()
 check(state.distance<5.2 and state.occluded and state.discovered,'approaching behind real cover still discovers marker')
 g:update(.025)
 check(g.secret_visible and g.saved.discovered[g.m.id]and not g.saved.earned['secret:'..g.m.id],'discovery cannot collect through cover')
 local near=g:treasure_state();g:load(1);state=g:treasure_state()
 check(state.discovered and state.visible and state.scale<near.scale,'discovery persists and nearby chest grows')
 local restored=fresh(1,g.saved)
 check(restored:treasure_state().discovered,'discovery survives a separate game reconstruction')
 local clues=#g.saved.clues;local speech;g.say=function(id)speech=id end;g:hint()
 check(#g.saved.clues==clues and speech=='defold_treasure_hint','already discovered chest is freely tracked again')
 -- Earned clue reveals the exact location persistently, with no second charge.
 g=fresh();g:award('mission:'..g.m.id);local credits=g:credits()
 g:hint();state=g:treasure_state()
 check(g:credits()==credits-1 and g:level()==1 and state.discovered and state.tracking,'earned clue reveals and tracks exact chest')
 local target=g:mission_state();check(target.goal[1]==sp[1]and target.goal[2]==sp[2],'paid clue compass uses actual chest position')
 g.hint_debounce=0;g:hint();check(g:credits()==credits-1,'repeating revealed clue cannot consume another credit')
 local before=#g.saved.clues;g:hint();check(#g.saved.clues==before,'debounced taps cannot double-charge')
 restored=fresh(1,g.saved);check(restored:treasure_state().discovered and restored:credits()==credits-1,'clue/discovery ledger survives reconstruction')
 for _,mode in ipairs({'paused','background','tactical_pause'})do
  g=fresh();g.p={sp[1],sp[2]};g[mode]=true;step(g,.25)
  check(not g.saved.earned['secret:'..g.m.id]and not g.saved.discovered[g.m.id],'no background discovery or pickup during '..mode)
 end
 -- Collection must have a clear live route, even inside the generous radius.
 g=fresh();g.m={id='reactor',secret={position={1,0},hint_landmark={1,0}}};g.p={0,0};g.walls={{r={.4,-.5,.1,1},type='cover'}}
 g:update_treasure();check(g:treasure_state().occluded and not g.saved.earned['secret:reactor'],'close chest cannot be collected across a thin wall')
 g.p={2,0};g:update_treasure();check(g.saved.earned['secret:reactor'],'same close chest collects from its accessible side')
 g=fresh();g.m={id='reactor',secret={position={1,0},hint_landmark={1,0}},gate_rect={.4,-.4,.2,.8}};g.p={0,0};g.walls={};g.clock=0
 g:update_treasure();check(not g.saved.earned['secret:reactor'],'closed live gate blocks close pickup')
 g.clock=5;g:update_treasure();check(g.saved.earned['secret:reactor'],'open live gate permits close pickup')
 g=fresh();g.m={id='reactor',secret={position={1,0},hint_landmark={1,0}}};g.p={0,0};g.walls={{r={.8,-.4,.4,.8},type='cover'}}
 g:update_treasure();check(not g.saved.earned['secret:reactor'],'invalid blocked chest never grants an impossible pickup')
 local store=saved();store.discovered={reactor=true,alien=true,dock='yes'}
 g=fresh(1,store);check(g.saved.discovered.reactor==true and g.saved.discovered.alien==nil and g.saved.discovered.dock==nil,'discovery migration keeps only valid mission booleans')
 store=saved();store.discovered=false;g=fresh(1,store)
 check(type(g.saved.discovered)=='table'and not g:treasure_state().discovered,'malformed old discovery field recovers safely')
 return n
end
return M
