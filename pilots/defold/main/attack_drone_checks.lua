-- Real attack-drone rules and gesture state, including stock and live walls.
-- GUI/native render tests add actual screen hit regions on top of these packets.
local Combat=require 'main.combat'
local Attack=require 'main.attack_drone'
local Controls=require 'main.drone_controls'
local M={}
local function dist(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh()
  local g=Combat.new(data);g:load(1)
  g.m={id=data.missions[1].id,kind='combat',attack_drone={stock=3,speed=7},covers={},reflectors={},exit_required=true,
   sanctuary={position={-8,5},radius=1.2},absorbers={}}
  g.arena={-10.5,-7.5,21,15};g.walls={};g.p={-6,0};g.path={};g.enemies={};g.fx={};g.paused=false;g.over=false;g.solved=false;g.background=false
  g.spoken={};g.say=function(id)g.spoken[#g.spoken+1]=id end
  Attack.bind(g);Attack.reset(g)
  return g
 end
 local function enemy(g,p,kind)
  local e={p={p[1],p[2]},hp=3,max_hp=3,kind=kind or'sentinel',timer=999,warning=0,direction={-1,0},burst=1}
  g.enemies[#g.enemies+1]=e;return e
 end
 local function choose(g,e)
  return g:drone_open()and g:drone_select()and g:drone_target(e)
 end
 local function step(g,seconds)
  for _=1,math.ceil(seconds/.025)do Attack.update(g,.025)end
 end
 for i,mission in ipairs(data.missions)do
  local g=Combat.new(data);g:load(i)
  if mission.attack_drone then
   check(g.attack_drone.enabled and g.attack_drone.stock==mission.attack_drone.stock,'configured finite stock loaded '..mission.id)
   local stock=g.attack_drone.stock;g:load(i)
   check(g.attack_drone.stock==stock and g.attack_drone.phase=='ready','retry restores mission stock without a saved currency '..mission.id)
  end
 end
 local g=fresh();local e=enemy(g,{4,0});local d=g.attack_drone
 check(d.stock==3 and d.max_stock==3 and d.phase=='ready','three ready devices, not a preplanted mine')
 g.held=true;g.aiming=true;g.pending_hold=true;g.path={{-4,0}}
 check(g:drone_open()and g.drone_ui.mode=='catalogue'and g.tactical_pause,'explicit stock catalogue freezes combat')
 check(not g.held and not g.aiming and not g.pending_hold and #g.path==0,'opening clears ordinary shooting and navigation')
 check(g.spoken[#g.spoken]=='defold_drone_open','catalogue has a matching complete instruction')
 check(not g:drone_target(e)and d.stock==3,'catalogue selection is required before targeting')
 check(g:drone_select()and g.drone_ui.mode=='target'and g.spoken[#g.spoken]=='defold_drone_target','selection explicitly asks for an enemy target')
 local score,wallet=g:total(),g:wallet();local p=g.p
 check(g:drone_target(e)and d.stock==2 and d.phase=='flying','valid target commits exactly one device')
 check(not g.drone_ui and not g.tactical_pause and g.spoken[#g.spoken]=='defold_drone_launch','flight resumes combat with matching feedback')
 check(g.p==p and #g.path==0 and d.p~=g.p and dist(d.p,g.p)==0,'planning preserves hero position and path, drone starts at hero')
 check(e.hp==3 and #g.fx==0,'launch does not teleport or directly award a kill')
 Attack.update(g,.025)
 check(e.hp==3 and dist(d.p,g.p)>.05 and dist(d.p,g.p)<=d.speed*.025+.001,'a real timed flight advances at finite speed')
 check(not g:drone_open()and d.stock==2,'a flying device cannot be duplicated by reopening')
 step(g,3)
 check(e.hp==0 and d.kills==1 and d.phase=='cooldown','actual contact destroys its target through the ordinary hit path')
 local electric=false;for _,fx in ipairs(g.fx)do electric=electric or fx.kind=='lightning'end
 check(electric and e.death_age==0,'contact emits electric animation plus the native death/explosion state')
 check(g:total()==score and g:wallet()==wallet,'launch and impact do not mint extra money')
 step(g,2.1);check(d.phase=='ready'and d.stock==2,'ready state returns after a bounded cooldown')
 g:load(1);check(g.attack_drone.stock==data.missions[1].attack_drone.stock,'mission reload resets transient stock only')

 for _,flag in ipairs({'paused','background','over'})do
  g=fresh();enemy(g,{4,0});g[flag]=true
  check(not g:drone_open()and g.attack_drone.stock==3 and not g.drone_ui,'no selection while '..flag)
 end
 g=fresh();e=enemy(g,{4,0});g.attack_drone.stock=0
 check(not g:drone_open()and g.spoken[#g.spoken]=='defold_drone_empty','empty stock explains the ordinary weapon/fallback')
 g=fresh();e=enemy(g,{4,0});g:drone_open();g:drone_select()
 local before=g.attack_drone.stock
 check(not g:drone_target(nil)and not g:drone_target({p={4,0},hp=3})and g.attack_drone.stock==before,'unknown pointers cannot become a target or consume stock')
 e.hp=0;check(not g:drone_target(e)and g.attack_drone.stock==before,'dead target cannot consume a device');e.hp=3
 e.optional=true;check(not g:drone_target(e),'optional puzzle targets cannot be bypassed');e.optional=nil
 e.kind='sequence';check(not g:drone_target(e),'sequence nodes are not attack-drone enemies');e.kind='sentinel'
 e.boss=true;local relay=enemy(g,{3,2},'relay')
 check(not g:drone_target(e)and g.attack_drone.stock==before and g.spoken[#g.spoken]=='defold_relays_free','boss relay lock is preserved without wasting stock')
 check(g:drone_target(relay),'relay itself is a legitimate tactical target')
 step(g,3);check(relay.hp==0 and e.hp==3,'drone can disable the protecting relay, not a locked boss')

 g=fresh();e=enemy(g,{4,0});g.walls={{r={3.8,-.4,.4,.8},type='cover'}}
 g:drone_open();g:drone_select();check(not g:drone_target(e)and g.attack_drone.stock==3,'target embedded in a wall cannot consume stock')
 g=fresh();e=enemy(g,{4,0})
 g.walls={{r={3,-1,.25,2.25},type='cover'},{r={4.75,-1,.25,2.25},type='cover'},
  {r={3,-1,2,.25},type='cover'},{r={3,1,2,.25},type='cover'}}
 g:drone_open();g:drone_select();check(not g:drone_target(e)and g.attack_drone.stock==3,'unreachable enclosed target has no free drone teleport')

 g=fresh();g.p={-4,0};e=enemy(g,{4,0});e.shield=true;e.trap_shield=true
 g.walls={{r={-.3,-2,.6,4},type='cover'}}
 local hero=g.p;local path=g.path
 check(choose(g,e)and #g.attack_drone.path>1,'route plans around the actual blocking wall')
 check(g.p==hero and g.path~=g.attack_drone.path and #g.path==0,'A-star never steals the hero route')
 local detour=false;local length=0;local previous={g.attack_drone.p[1],g.attack_drone.p[2]}
 for frame=1,240 do
  Attack.update(g,.025)
  local point=g.attack_drone.p
  check(not g:blocked(point),'flight stays on free floor at frame '..frame)
  local moved=dist(previous,point);check(moved<=g.attack_drone.speed*.025+.001,'flight cannot jump across a wall at frame '..frame)
  detour=detour or math.abs(point[2])>2;length=length+moved;previous={point[1],point[2]}
  if e.hp<=0 then break end
 end
 check(detour and length>8 and e.hp==0,'a real collision-safe detour reaches and destroys shielded target')
 check(g.p==hero and e.shield==true,'flight preserves hero and does not permanently mutate shield metadata')

 g=fresh();g.p={0,0};e=enemy(g,{5,0});check(choose(g,e),'start flight before a gate closes')
 Attack.update(g,.025);g.walls={{r={1,-7.5,.3,15},type='gate'}}
 step(g,1);check(g.attack_drone.p[1]<1 and e.hp==3,'a newly closed live wall stops flight instead of being crossed')
 g.walls={};step(g,3);check(e.hp==0,'opening the route lets the same drone continue')

 g=fresh();e=enemy(g,{4,0});check(choose(g,e),'flight can track a live moving enemy')
 step(g,.3);e.p={7,1};step(g,4)
 check(e.hp==0 and g.attack_drone.kills==1,'drone replans to the moving target, not its old coordinates')
 g=fresh();e=enemy(g,{4,0});choose(g,e);e.hp=0;Attack.update(g,.025)
 check(g.attack_drone.stock==3 and g.attack_drone.kills==0,'already destroyed target returns the unused device')
 g=fresh();e=enemy(g,{4,0});choose(g,e);g.attack_drone.age=g.attack_drone.timeout;Attack.update(g,.025)
 check(g.attack_drone.stock==3 and g.attack_drone.phase=='cooldown'and e.hp==3,'flight lifetime is finite and a failed route returns stock')

 g=fresh();g.p={0,0};e=enemy(g,{4,0});local near=enemy(g,{3.6,1.6});local hidden=enemy(g,{5.3,0});local node=enemy(g,{3.8,-1.5},'sequence')
 g.walls={{r={4.5,-.5,.2,1},type='cover'}};choose(g,e);step(g,3)
 check(e.hp==0 and near.hp==3 and near.trapped>=3,'impact destroys only its chosen target and jams nearby enemies')
 check(not hidden.trapped and not node.trapped,'electronic disruption cannot pass through cover or solve sequence nodes')
 g=fresh();e=enemy(g,{4,0});choose(g,e);local age=g.attack_drone.age;local position={g.attack_drone.p[1],g.attack_drone.p[2]}
 for _,flag in ipairs({'paused','background','over','tactical_pause'})do
  g[flag]=true;Attack.update(g,2);g[flag]=false
  check(g.attack_drone.age==age and dist(g.attack_drone.p,position)==0 and e.hp==3,'flight is frozen while '..flag)
 end
 g=fresh();g.arena={-21,-15,42,30};g.p={-16,8};e=enemy(g,{18,-10});choose(g,e);step(g,9)
 check(e.hp==0 and g.attack_drone.kills==1,'finite flight works across the largest configured mission arena')

 local function controller()
  local game=fresh();local target=enemy(game,{4,0})
  local c=Controls.new(game,function(x,y)if math.abs(x-600)<=40 and math.abs(y-300)<=40 then return target end end,nil,
   function(x,y)return x>144 and x<1136 and y>96 and y<624 end)
  game.drone_control=c
  check(c:open()and c:select(),'controller selects a stock device before target gestures')
  game.drone_ui.rect={300,300,90,90}
  return game,c,target
 end
 g,d,e=controller();d:input({x=600,y=300,id=1,pressed=true})
 check(g.attack_drone.phase=='flying'and g.attack_drone.stock==2 and d:blocks_input(),'one generous enemy press launches immediately and owns its tail')
 d:input({x=600,y=300,id=2,pressed=true});d:input({x=600,y=300,id=1,released=true})
 check(d:blocks_input()and g.attack_drone.stock==2,'another held finger cannot become an extra launch or shot')
 d:input({x=600,y=300,id=2,released=true})
 check(not d:blocks_input()and g.shots_fired==0 and #g.path==0,'both contact tails drain without an ordinary shot or step')
 g,d,e=controller();d:input({x=300,y=300,id=1,pressed=true});d:input({x=600,y=300,id=1})
 check(g.drone_ui.dragging and g.drone_ui.x==600 and g.attack_drone.stock==3,'drag previews an attack without placing a mine or consuming stock')
 d:input({x=600,y=300,id=2,released=true})
 check(g.attack_drone.stock==3 and d.pointer~=nil,'foreign release cannot drop the owned drone')
 d:input({x=600,y=300,id=1,released=true})
 check(g.attack_drone.phase=='flying'and g.attack_drone.stock==2 and not d:blocks_input(),'owned drop onto enemy launches exactly once')
 g,d,e=controller();d:input({x=300,y=300,id=1,pressed=true});d:input({x=700,y=450,id=1,released=true})
 check(g.drone_ui.mode=='target'and not g.drone_ui.dragging and g.attack_drone.stock==3,'dropping onto empty floor keeps target choice without consuming stock')
 d:input({x=600,y=300,id=1,pressed=true});check(g.attack_drone.stock==2,'direct target tap remains available after an invalid drag')
 g,d,e=controller();d:input({x=300,y=300,id=1,pressed=true});d:cancel(false)
 check(not g.drone_ui and not g.tactical_pause and d:blocks_input(),'explicit cancellation closes mode while swallowing its held tail')
 d:input({x=600,y=300,id=1,released=true});check(not d:blocks_input()and g.attack_drone.stock==3,'cancelled drop cannot launch')
 g,d,e=controller();d:input({x=300,y=300,id=1,pressed=true});d:reset();d:input({x=600,y=300,id=1,released=true})
 check(not g.drone_ui and not d:blocks_input()and g.attack_drone.stock==3,'focus/load hard reset cannot preserve a stale launch pointer')
 g,d,e=controller();d:input({x=1200,y=300,id=1,pressed=true});d:input({x=600,y=300,id=1,released=true})
 check(g.attack_drone.stock==3,'gesture beginning outside the map cannot target from a neutral HUD/letterbox')
 for _,flag in ipairs({'paused','background','over'})do
  g,d,e=controller();d:input({x=300,y=300,id=1,pressed=true});g[flag]=true;d:input({x=600,y=300,id=1,released=true})
  check(g.attack_drone.stock==3 and not g.drone_ui,'drag cannot launch during '..flag)
 end
 return n
end
return M
