-- Executed in the native Defold process against the shipped six-sector rules.
local C=require 'main.combat'
local Layout=require 'main.layout'
local Progression=require 'main.progression'
local P=require 'main.projectiles'
local M={}
function M.run(g)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function step(seconds)for i=1,math.floor(seconds/.025+.001)do g:update(.025)end end
 local function fresh(i)g.saved={earned={},clues={},weapon='pulse',schema=2,purchases={},spent={}};g:load(i or 1);for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0 end end
 local function fire_at(t)local p=t.p;g.aim=C.norm({p[1]-g.p[1],p[2]-g.p[2]});g.cooldown=0;g:fire();step(.25)end
 local surfaces=json.decode(sys.load_resource('/data/surfaces.json'))
 check(#g.data.missions==6,'six selectable sectors')
 for i,m in ipairs(g.data.missions)do
  fresh(i);local rows=surfaces[m.id];check(#rows==#g.walls,'rendered surface count matches collision count '..m.id)
  local match=true
  for j,w in ipairs(g.walls)do if w.type~=rows[j].type then match=false end;for k=1,4 do if math.abs(w.r[k]-rows[j].r[k])>1e-7 then match=false end end end
  for j,w in ipairs(g.walls)do for k=1,4 do if math.abs(w.r[k]-rows[j].geometry_r[k])>.00001 then match=false end end end
  check(match,'every static wall uses its exact generated footprint '..m.id)
  check(#m.secret.marks>=2,'free environmental treasure clues '..m.id)
  for _,mark in ipairs(m.secret.marks)do check(not g:blocked(mark.position),'trail is on walkable floor '..m.id)end
  check(not g:blocked(m.secret.position),'treasure reachable '..m.id)
 end
 for id,r in pairs(Layout.controls)do check(Layout.safe(r[1],r[2],r[3],r[4]),'control outside scene '..id)end
 check(not Layout.field(300,Layout.bottom)and not Layout.field(300,Layout.top),'viewport border cannot start movement')
 fresh();check(g:wallet()==0 and not g:owns('armor'),'fresh shop starts empty')
 g:award('mission:reactor');g:award('skill:reactor');check(g:total()==100 and not g:owns('prism')and g.saved.weapon=='pulse','stars do not silently buy equipment')
 check(g:buy('prism')and g:owns('prism')and g:wallet()==0 and g:total()==100,'real purchase debits balance but retains lifetime score')
 check(not g:buy('armor')and not g:owns('armor')and g:wallet()==0,'insufficient funds cannot purchase')
 check(not g:buy('unknown')and g:wallet()==0,'unknown item cannot spend money')
 g:buy('prism');check(g:wallet()==0 and g.saved.weapon=='pulse','owned weapon toggles without paying twice');g:buy('prism')
 for k in pairs(g.data.rewards)do if not k:match(':bank$')and not k:match(':guardian$')then g:award(k)end end
 check(g:total()==1200 and g:wallet()==1100,'six sectors have bounded one-time rewards')
 check(g:buy('armor')and g.max_hp==4,'armor purchase adds one health immediately')
 check(g:buy('boots')and g:buy('cloak')and g:wallet()==410,'remaining gear can be bought through play')
 g:load(1);check(g.max_hp==4 and g:owns('boots')and g:owns('cloak'),'gear remains equipped on sector restart')
 local stored=g.saved;local restored=C.new(g.data,stored);check(restored:wallet()==410 and restored:total()==1200 and restored.max_hp==4,'purchase state survives reconstruction')
 local old={earned={['mission:dock']=true,['skill:dock']=true,['mission:reactor']=true,['skill:reactor']=true},clues={},weapon='prism'}
 local migrated=C.new(g.data,old);check(migrated:total()==300 and migrated:wallet()==300 and migrated:owns('cloak')and migrated:owns('armor'),'old automatic unlocks migrate without loss or charge')
 migrated.saved.purchases.boots=nil;Progression.bind(migrated);check(not migrated:owns('boots'),'migration cannot repeatedly mint equipment')
 fresh();check(g:set_character('dragon')and g:character().shot=='fireball','dragon selected')
 g:fire();check(g.bullets[1].visual=='fireball'and g.bullets[1].max_bounces==1,'dragon fireball keeps physical limits')
 check(not g:set_character('internet-character')and g:character().id=='dragon','invalid character rejected')
 g:set_character('fox');g:load(2);check(g:character().id=='fox','character selection persists across missions')
 fresh(4);local t=g.enemies[1];g:hit(t,0);g:hit(t,1);check(t.hp==3,'trap guardian cannot be beaten by firing into its shield')
 g.p={3,-4};check(g:trap()and #g.traps==1,'place magnet trap')
 check(not g:trap()and #g.traps==1,'trap has real cooldown')
 g.p={3,-2.8};step(2.3);check(t.trapped>2 and #g.traps==0,'live patrol enters trap and loses shield')
 fire_at(t);g.cooldown=0;fire_at(t);g.cooldown=0;fire_at(t);check(g.solved and t.hp==0,'prepared trap creates an actual firing opportunity and completion')
 fresh(4);g.p={-7,5};g:trap();step(12.2);check(#g.traps==0,'unused traps expire')
 fresh(5);local function crystal(id)for _,e in ipairs(g.enemies)do if e.kind=='sequence'and e.order==id then return e end end end
 local a,b,c=crystal(1),crystal(2),crystal(3)
 g:hit(a,0);check(g.sequence_progress==0 and a.hp==1,'wrong first crystal resets without granting points')
 g:hit(b,0);g:hit(c,0);check(g.sequence_progress==0 and b.hp==1 and c.hp==1,'wrong later crystal resets entire sequence')
 for _,id in ipairs(g.m.sequence)do local e=crystal(id);g.p={e.p[1],e.p[2]+.8};fire_at(e)end
 check(g.sequence_progress==3 and a.hp==0 and b.hp==0 and c.hp==0,'actual shots complete the observed light sequence')
 check(not g.solved,'sequence does not bypass the active cannon')
 t=g.enemies[1];g.p={t.p[1],t.p[2]+.8};fire_at(t);fire_at(t);check(g.solved,'sequence plus cannon completes the sector')
 fresh(6);local drone=g.drone;g.p={7,5};step(1);check(drone.waypoint==1 and not drone.moving,'drone waits when escort leaves it behind')
 g.p=g.m.goal;g.clock=5;step(.05);check(not g.solved,'going to exit without drone cannot win')
 -- Swept enemy projectile really damages the escorted drone.
 g.p={-8,5};P.spawn(g,{drone.p[1],drone.p[2]-1},{0,1},true);step(.2)
 check(drone.hp==2 and g.damage==0,'enemy shot hits drone rather than player')
 local guard=0
 while not g.solved and guard<1600 do g.p={drone.p[1],drone.p[2]+.9};g:update(.025);guard=guard+1 end
 check(g.solved and drone.arrived and drone.waypoint==5,'full escorted route reaches goal without crossing cover')
 check(g.reward==125,'damaged escort does not receive the perfect-protection bonus')
 local total=g:total();g:finish();check(g:total()==total,'new mission cannot farm completion rewards')
 fresh(6);g.drone.invulnerable=0;g:hit_drone();g.drone.invulnerable=0;g:hit_drone();g.drone.invulnerable=0;g:hit_drone();check(g.dialog=='defeat'and g.drone.hp==0,'lost drone offers a real retry')
 return n
end
return M
