-- Current trap assistance is earned across distinct completed missions. These
-- checks exercise actual placement, triggering, completion and save reconstruction.
local Combat=require 'main.combat'
local O=require 'main.objectives'
local Controls=require 'main.trap_controls'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function near(a,b)return math.abs(a-b)<.00001 end
 local function fresh(index,store)
  local g=Combat.new(data,store);g:load(index or 4)
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil end
  g.invulnerable=999;g.trap_control=Controls.new(g,function(x,y)return{x,y}end)
  return g
 end
 local function tick(g,seconds)
  for _=1,math.floor(seconds/.025+.001)do g:update(.025)end
 end
 local function trigger(g,id)
  local e=g.enemies[1];g.p={0,-4};e.p={0,-4};e.patrol=nil;e.timer=999;e.warning=0
  g.path={};g.trap_cooldown=0
  check(g:trap(g.p,id),'real current trap can be planted '..id)
  g:update(.025)
  check(#g.traps==0 and(e.trapped or 0)>0,'live main enemy actually triggers '..id)
  return e
 end
 local function finish_forge(g)
  local e=trigger(g,'magnet')
  for _=1,e.hp do g:hit(e,0)end
  check(g.solved and g.saved.earned['mission:forge'],'real shield opening and hits complete forge')
 end
 local g=fresh()
 check(near(Controls.range_for(g),5.25)and near(O.trap_range(g),5.25),'visible circle and validator share enlarged 5.25-unit radius')
 check(O.trap_timing(g).multiplier==3 and O.trap_timing(g).armed_lifetime==36,'first trap lesson triples effect and armed waiting time')
 for _,spec in ipairs(O.catalogue)do
  local effective=O.trap_spec(spec.id,g)
  check(effective.duration==spec.duration*3 and effective.armed_lifetime==36,'tripled current duration '..spec.id)
  check(effective.cooldown==spec.cooldown and effective.radius==spec.radius,'recharging and trigger radius unchanged '..spec.id)
 end
 check(O.catalogue[1].duration==6 and O.catalogue[2].duration==9 and O.catalogue[3].duration==5,'current timing never mutates historical catalogue')
 for i=1,#data.missions do
  local mission=fresh(i)
  check(O.can_trap(mission)==(i>=4),'trap availability matches lesson progression '..i)
  check(mission.trap_control:open()==(i>=4),'actual catalogue opens in eligible later mission '..i)
 end
 -- An empty local test corridor isolates exact circle boundaries, not the old
 -- phone-sized tap zone. Actual free-floor and wall checks still run below.
 g=fresh();g.walls={};g.p={0,0};local c=g.trap_control
 check(c:valid({4.5,0}),'floor beyond old 3.5-unit circle is now valid')
 check(c:valid({5.25,0}),'visible circle boundary is included')
 check(not c:valid({5.251,0})and not g:trap({5.251,0},'magnet'),'beyond visible circle rejected by UI and direct gameplay')
 check(g:trap({5.25,0},'magnet')and near(g.traps[1].life,36),'direct gameplay accepts same boundary and full armed duration')
 g=fresh();g.walls={};g.p={0,0};g.walls={{r={1,-1,.2,2},type='cover'}}
 local ok,reason=g.trap_control:valid(nil)
 check(not ok and reason=='HIER IST EINE WAND','missing floor point rejected safely')
 ok,reason=g.trap_control:valid({1.1,0})
 check(not ok and reason=='HIER IST EINE WAND'and not g:trap({1.1,0},'magnet'),'solid floor cannot contain trap')
 ok,reason=g.trap_control:valid({2,0})
 check(not ok and reason=='WAND DAZWISCHEN'and not g:trap({2,0},'magnet'),'inside circle does not permit placement through cover')
 check(not g.trap_control:valid({math.huge,0})and not g.trap_control:valid({0/0,0}),'non-finite floor cannot bypass circle')
 -- A planted device remains available for the promised waiting time.
 g=fresh();g.enemies={};g.walls={};g.p={0,0}
 check(g:trap({1,0},'magnet'),'unused device planted')
 tick(g,12.5);check(#g.traps==1,'unused device survives former 12-second expiry')
 tick(g,23.4);check(#g.traps==1 and g.traps[1].life>0,'unused device lasts almost all 36 seconds')
 tick(g,.2);check(#g.traps==0,'unused device still expires after extended waiting time')
 for _,id in ipairs({'magnet','frost','pulse'})do
  g=fresh();local e=trigger(g,id);local expected=O.trap_spec(id,g).duration
  check(near(e.trapped,expected-.025),'actual triggered duration is tripled '..id)
  check(not g.saved.trap_practice.forge and g.trap_success_this_round,'trigger without completion grants no permanent mastery '..id)
 end
 g=fresh();local e=trigger(g,'frost');local stopped=e.timer
 tick(g,9.5);check(e.trapped>17 and e.timer==stopped,'ice still holds and suppresses attacks beyond former nine seconds')
 tick(g,17.4);check(e.trapped>0 and e.timer==stopped,'ice preserves almost the entire promised27-second firing window')
 tick(g,.2);check(e.trapped==0 and e.timer<stopped,'guardian only resumes after the extended ice duration ends')
 g=fresh();g.enemies={};g.walls={};g.p={0,0};g:trap({0,0},'magnet');g.traps[1].life=.01
 e={p={0,0},hp=3,max_hp=3,timer=999,warning=0,direction={1,0}};g.enemies={e};g:update(.025)
 check(#g.traps==0 and not g.trap_success_this_round and(e.trapped or 0)==0,'expired device cannot trigger on its final elapsed update')
 -- A wall also blocks a trap's small activation radius; it cannot immobilise a
 -- guardian on the other side simply because its centre is near the device.
 g=fresh();g.p={0,0};g.walls={};e=g.enemies[1];e.p={.7,0};e.patrol=nil
 check(g:trap({0,0},'magnet'),'near-wall test trap planted on free floor')
 g.walls={{r={.3,-1,.1,2},type='cover'}};g:update(.025)
 check(#g.traps==1 and not g.trap_success_this_round and(e.trapped or 0)==0,'solid wall blocks activation across it')
 -- Assistance never falls just from entering, abandoning or replaying a sector.
 g=fresh();trigger(g,'magnet');g:load(5)
 check(O.trap_timing(g).multiplier==3 and not g.saved.trap_practice.forge,'abandoned real trap attempt cannot reduce help')
 local store={earned={['mission:forge']=true,['mission:echo']=true},clues={},schema=3,purchases={},spent={}}
 g=fresh(6,store)
 check(O.trap_timing(g).multiplier==3,'old completed saves without trap evidence keep full assistance')
 g=fresh();finish_forge(g);store=g.saved
 check(store.trap_practice.forge==true,'successful completed trap lesson persists its evidence')
 check(O.trap_timing(g).multiplier==3,'completion does not shorten current round snapshot')
 g=fresh(5,store)
 check(O.trap_timing(g).multiplier==2.5 and O.trap_timing(g).armed_lifetime==30,'one trained earlier mission gently lowers later help to 2.5x')
 check(O.trap_spec('magnet',g).duration==15 and O.trap_spec('frost',g).duration==22.5 and O.trap_spec('pulse',g).duration==12.5,'second-stage effective times are exact')
 g:finish();g=fresh(6,g.saved)
 check(O.trap_timing(g).multiplier==2.5 and not g.saved.trap_practice.echo,'completion without using traps does not reduce assistance')
 -- Complete the echo mission through its real final sequence after using a trap.
 g=fresh(5,store);trigger(g,'magnet')
 for _,enemy in ipairs(g.enemies)do if not enemy.optional and enemy.kind~='sequence'then while enemy.hp>0 do g:hit(enemy,1)end end end
 for _,order in ipairs(g.m.sequence)do for _,enemy in ipairs(g.enemies)do if enemy.kind=='sequence'and enemy.order==order then g:hit(enemy,0);break end end end
 check(g.solved and g.saved.trap_practice.echo==true,'second actual trap use and sequence completion save second evidence')
 check(O.trap_timing(g).multiplier==2.5,'second mission keeps its loaded timing after completion')
 store=g.saved;g=fresh(6,store)
 check(O.trap_timing(g).multiplier==2 and O.trap_timing(g).armed_lifetime==24,'two distinct trained earlier lessons reduce next mission to 2x')
 check(O.trap_spec('magnet',g).duration==12 and O.trap_spec('frost',g).duration==18 and O.trap_spec('pulse',g).duration==10,'third-stage effective times remain generous')
 g=fresh(4,store)
 check(O.trap_timing(g).multiplier==3,'replaying first lesson retains first-lesson help')
 local total=g:total();finish_forge(g)
 check(g:total()==total,'replayed completed trap mission cannot mint stars')
 g=fresh(5,g.saved);check(O.trap_timing(g).stage==2,'repeating same trained mission cannot count twice')
 store.trap_practice={forge=true,echo=true,rescue='true',reactor=true,unknown=true}
 g=fresh(6,store)
 check(g.saved.trap_practice.forge and g.saved.trap_practice.echo and not g.saved.trap_practice.rescue and not g.saved.trap_practice.reactor and not g.saved.trap_practice.unknown,'practice save sanitizes booleans and eligible mission IDs')
 store.trap_practice=false;g=fresh(6,store)
 check(type(g.saved.trap_practice)=='table'and O.trap_timing(g).multiplier==3,'malformed practice save safely preserves generous baseline')
 return n
end
return M
