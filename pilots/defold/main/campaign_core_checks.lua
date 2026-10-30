-- Active campaign contracts, including migrations and bounded live swarms.
local Combat=require 'main.combat'
local Shots=require 'main.projectiles'
local Swarm=require 'main.swarm'
local M={}
local function copy(value)
 if type(value)~='table'then return value end
 local result={};for k,v in pairs(value)do result[k]=copy(v)end;return result
end
function M.run(source)
 if not source.campaign_enabled then return 0 end
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(index,saved)
  local g=Combat.new(copy(source),saved or{earned={},clues={},schema=3,purchases={},spent={},weapon='pulse'})
  g:load(index or 1)
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil end
  return g
 end
 local function step(g,seconds)
  for _=1,math.floor(seconds/.025+.001)do g:update(.025)end
 end
 local function funded(all_missions)
  local saved={earned={},clues={'reactor:1'},schema=3,purchases={armor=true,armor2=true,armor3=true,armor4=true,prism=true,arc=true,nova=true,nova2=true,cloak=true,cloak2=true},spent={armor=160,armor2=300,armor3=450,armor4=650,prism=100,arc=220,nova=400,nova2=650,cloak=300,cloak2=450},weapon='nova2',character='dragon',music=false}
  for key in pairs(source.rewards)do
   if all_missions or not key:match('^mission:')and not key:match('^skill:')then saved.earned[key]=true end
  end
  return saved
 end
 for index,mission in ipairs(source.missions)do
  local g=fresh(index);local z=mission.sanctuary
  check(g.arena==g.m.arena or g.arena==g.data.arena,'mission bounds are the active simulation bounds '..mission.id)
  check(g.max_hp==20 and g.hp==20,'fresh campaign health begins at twenty '..mission.id)
  check(Combat.dist(g.p,z.position)<.00001 and g:is_safe(),'mission starts inside its protected Zikkurat '..mission.id)
  check(not g:blocked(g.p),'protected spawn remains walkable '..mission.id)
  check(g.bonus.total==0 and #g.bonus.tasks==0 and not g.secret_visible and not g:treasure_state().available,'no hidden bonus or chest objective survives '..mission.id)
  local optional=0;for _,e in ipairs(g.enemies)do if e.optional then optional=optional+1 end end
  check(optional==0 and Swarm.alive(g)<=50,'initial objective population is bounded and contains no bonus targets '..mission.id)
  local before=g:credits();local speech;g.say=function(id)speech=id end;g:hint()
  check(g:credits()==before and speech and not speech:match('bonus')and not speech:match('treasure'),'hint only explains mission work without spending clues '..mission.id)
  local hp,shield=g.hp,g.shield;g:hit_player();g:fire()
  check(g.hp==hp and g.shield==shield and g.shots_fired==0,'protected start absorbs damage and does not fire outward '..mission.id)
  Shots.spawn(g,g.p,{1,0},true);Shots.update(g,.025)
  check(g.hp==hp and #g.bullets==0 and g.sanctuary_absorbed==1,'even a hostile shot spawned in the refuge is absorbed '..mission.id)
  local a=g.arena
  check(g:blocked({a[1]-.1,a[2]+a[4]/2})and g:blocked({a[1]+a[3]+.1,a[2]+a[4]/2}),'individual larger arena edges still block movement '..mission.id)
 end
 -- Permanent progression now follows missions, never old hidden bonus fields.
 local saved=funded(false);local g=fresh(1,saved);local balance,total=g:wallet(),g:total()
 check(g:power_state().count==0 and g:power_state().total==16,'only the sixteen known mission completions determine progress')
 check(g.max_hp==40 and g.max_hp<=100,'old million bonus save becomes capped campaign gear without erasing ownership')
 check(g:owns('armor4')and g:owns('nova2')and g:character().id=='dragon'and not g.saved.music,'old purchases hero and preferences survive the rules change')
 check(g:total()==total and g:wallet()==balance and g.saved.spent.armor4==650,'old star rewards and debits remain unchanged')
 check(g:award('bonus:prism:reactor')==0 and g:award('secret:reactor')==0,'removed hidden reward keys can never be newly farmed')
 g=fresh(1,funded(true))
 check(g.max_hp==100 and g.hp==100 and g:power_state().count==16,'all missions and highest armor stop at exactly one hundred')
 check(g.max_shield<=20 and g:weapon_stats().damage<=8 and g:weapon_stats().cooldown>=.16,'shield damage and cadence remain bounded')
 local gear=g:detection_multiplier()
 g.saved.purchases.cloak2=nil;local first=g:detection_multiplier();g.saved.purchases.cloak=nil;local none=g:detection_multiplier()
 check(gear>=.55 and gear<first and first<none and none<=1,'both cloak upgrades remain useful without removing all detection')
 local unknown=copy(g.saved);unknown.earned['mission:invented']=true;unknown.earned['bonus:invented']=true
 local rebuilt=fresh(1,unknown)
 check(rebuilt:power_state().count==16 and rebuilt.max_hp==100,'unknown old save keys cannot exceed campaign health cap')
 -- Do not take stars for armor that cannot improve the capped maximum.
 g=fresh(1,funded(true));g.saved.purchases={};g.saved.spent={};g.saved.weapon='pulse'
 g:load(1);balance=g:wallet()
 local allowed,reason=g:can_buy('armor');local row=g:shop_item('armor')
 check(not allowed and reason=='GESUNDHEIT BEREITS MAXIMAL'and not row.available,'ineffective armor is visibly unavailable at capped health')
 check(not g:buy('armor')and g:wallet()==balance,'ineffective armor cannot consume wallet balance')
 -- Each new completed mission grows the current round once, preserving damage.
 g=fresh();g.hp=15
 local maximum=g.max_hp;local before=g:total();local earned=g:award('mission:reactor')
 check(earned==source.rewards['mission:reactor']and g:power_state().count==1,'real mission reward advances mission-based progress once')
 check(g.max_hp==25 and g.hp==20 and g.max_hp-g.hp==maximum-15,'health growth preserves existing damage rather than erasing it')
 local hp=g.hp;check(g:award('mission:reactor')==0 and g.hp==hp,'replayed completion cannot heal or advance progression')
 check(g:total()==before+earned and g.power_flash>0,'completion grants only its normal stars and current growth feedback')
 g=fresh();g.hp=0;g.over=true;g:award('mission:reactor')
 check(g.hp==0 and g.over,'a stored completion does not revive a defeated player')
 -- Real shield hits and recharge, with pause/focus accounting.
 g=fresh(1,funded(true));g.p={0,0};g.walls={};g.enemies={};g.max_shield=20;g.shield=20
 local old_hp=g.hp;g:hit_player()
 check(g.hp==old_hp and g.shield==19,'shield absorbs a genuine hit before health')
 for _=1,20 do g.invulnerable=0;g:hit_player()end
 check(g.shield==0 and g.hp==old_hp-1 and g.damage==1,'exhausted shield allows real health damage')
 step(g,3.6);check(g.shield>0 and g.shield<=20,'shield recharges after its real delay and stops at twenty')
 for _,mode in ipairs({'paused','background','tactical_pause'})do
  g=fresh(1,funded(true));g.enemies={};g.hp=40;g.shield=1;g[mode]=true
  step(g,10);check(g.hp==40 and g.shield==1,'no recovery occurs during '..mode)
 end
 -- Maximal cloaking still permits an accurate long-range periodic sensor shot.
 g=fresh(16,funded(true));g.arena={-21,-15,42,30};g.walls={};g.p={20,14};g.path={};g.bullets={};g.max_shield=0;g.shield=0
 g.m=copy(g.m);g.m.sanctuary={position={-19,12},radius=1.2};g.m.absorbers={};g.m.gate_rect=nil
 local enemy={p={-20,-14},hp=3,max_hp=3,kind='sentinel',timer=0,warning=0,direction={1,0},burst=1}
 g.enemies={enemy};Swarm.initialize(g);enemy.scan_clock=.01
 g:update(.025)
 local expected=Combat.norm({40,28})
 check(enemy.warning>0 and enemy.sensor_lock,'maximal cloak is located from the opposite corner of the largest arena')
 check(math.abs(enemy.direction[1]-expected[1])<.000001 and math.abs(enemy.direction[2]-expected[2])<.000001,'far sensor aims at the actual current player position')
 step(g,source.combat.enemy_warning+.1)
 local b=g.bullets[1]
 check(b and b.sensor_lock and b.speed==8 and b.lifetime==8 and b.remaining<=64 and b.remaining>50,'long-range sensor shot has adequate but finite speed lifetime and range')
 enemy.timer=999;step(g,6.4)
 check(g.damage==1 and g.hp<100,'the accurate far shot actually reaches and hits an unshielded player')
 -- A full fifty-enemy firing frame cannot allocate an unbounded projectile swarm.
 g=fresh(16,funded(true));g.arena={-21,-15,42,30};g.walls={};g.p={19,13};g.path={};g.bullets={}
 g.m=copy(g.m);g.m.sanctuary={position={-19,12},radius=1.2};g.m.absorbers={};g.m.gate_rect=nil;g.enemies={}
 for i=1,50 do g.enemies[#g.enemies+1]={p={-18+(i%10)*1.6,-12+math.floor(i/10)*1.8},hp=2,max_hp=2,kind='sentinel',timer=0,warning=.01,direction={1,0},burst=3}end
 Swarm.initialize(g)
 for _,e in ipairs(g.enemies)do e.sensor_lock=true end
 g:update(.025)
 check(#g.bullets==32,'simultaneous shots from fifty enemies respect the global thirty-two projectile budget')
 local bounded=true
 for _=1,240 do g:update(.025);local count=0;for _,shot in ipairs(g.bullets)do if shot.enemy then count=count+1 end end;if count>32 then bounded=false;break end end
 check(bounded,'the hostile projectile limit remains true during sustained fifty-enemy combat')
 -- Safe refuge overrides periodic detection as well as ordinary damage.
 g=fresh(16,funded(true));g.p=copy(g.m.sanctuary.position);g.bullets={};enemy=g.enemies[1];enemy.timer=0;enemy.scan_clock=0;enemy.warning=.01;enemy.sensor_lock=true
 g:update(.025)
 check(#g.bullets==0 and enemy.warning==0 and not enemy.sensor_lock,'periodic targeting never fires into an occupied Zikkurat')
 -- A simple empty arena isolates finite replication while using real combat hits.
 g=fresh(16);g.arena={-21,-15,42,30};g.m=copy(g.m);g.m.id='cap-fixture';g.m.exit_required=false;g.m.sequence=nil;g.m.gate_rect=nil;g.m.absorbers={};g.m.sanctuary={position={-19,12},radius=1.2};g.p=copy(g.m.sanctuary.position);g.walls={};g.enemies={};g.bullets={}
 for i=1,20 do
  g.enemies[#g.enemies+1]={p={-6+(i%5)*2,-6+math.floor(i/5)*2},hp=2,max_hp=2,kind='splitter',timer=999,warning=0,direction={1,0},burst=1,source_spec={kind='splitter',replication_period=8,max_generation=2}}
 end
 Swarm.initialize(g)
 local peak=Swarm.alive(g)
 for frame=1,420 do
  g:update(.05);peak=math.max(peak,Swarm.alive(g))
  if frame%20==0 then check(Swarm.alive(g)<=50,'live swarm cap holds during timed spread '..frame)end
 end
 check(peak==50 and g.swarm_spawned>=30,'swarm genuinely spreads and reaches, but never exceeds, fifty live enemies')
 local ids={}
 for _,e in ipairs(g.enemies)do
  check(e.uid and not ids[e.uid],'dynamic enemies receive distinct stable identities');ids[e.uid]=true
  check(not g:blocked(e.p)and Combat.dist(e.p,g.m.sanctuary.position)>g.m.sanctuary.radius,'new drone stays on valid floor outside the safe refuge')
 end
 local kills=0
 while not g.solved and kills<180 do
  local target
  for _,e in ipairs(g.enemies)do if e.hp>0 then target=e;break end end
  if not target then break end
  g:hit(target,1,target.hp);kills=kills+1
  check(Swarm.alive(g)<=50,'death splitting cannot exceed the live enemy cap '..kills)
 end
 check(g.solved and kills<=140,'finite two-generation families can all be defeated and the mission finishes')
 check(g.swarm_spawned<=120,'one parent cannot spawn the same family twice at death')
 -- Retirement hands native objects back to the renderer after the death window.
 g=fresh(1);g.enemies={};local dead={p={0,0},hp=0,max_hp=1,death_age=1.3,kind='mini_drone',uid=99}
 g.enemies[1]=dead;g.retired_enemies={};Swarm.update(g,.025)
 check(#g.enemies==0 and g.retired_enemies[1]==dead,'expired dead entities are explicitly handed to native cleanup')
 g=fresh(1);g.walls={{r={.35,-4,.2,8},type='cover'}};g.enemies={};g.m.sanctuary={position={-8,5},radius=1.2}
 check(not Swarm.free(g,{1,0},{0,0}),'replication cannot cross a real intervening wall')
 check(not Swarm.free(g,{-8,5},{-8,4}),'replication cannot enter a protected spawn')
 return n
end
return M
