-- Current rules only: recovery, impenetrable refuge and a persistent tier shop.
local Combat=require 'main.combat'
local Shots=require 'main.projectiles'
local M={}
function M.run(data)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function saved()return{earned={},clues={},weapon='pulse',schema=3,purchases={},spent={}}end
 local function fresh(index,store)
  local g=Combat.new(data,store or saved());g:load(index or 1)
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0 end
  return g
 end
 local function quiet(g)g.enemies={};g.bonus={tasks={},total=0,completed=0}end
 local function step(g,t)for i=1,math.floor(t/.025+.001)do g:update(.025)end end
 local function funded()
  local s=saved();for key in pairs(data.rewards)do s.earned[key]=true end
  return fresh(1,s)
 end
 local g=fresh();check(g.hp==15 and g.max_hp==15,'five times the previous unarmored health')
 local s=saved();s.schema=2;s.purchases={armor=true,boots=true,prism=true};s.spent={armor=160,boots=230,prism=100};s.weapon='prism'
 g=fresh(1,s)
 check(g.max_hp==20 and g:owns('boots')and g.saved.weapon=='prism','old armor receives fivefold health and boots/weapon survive')
 check(g.saved.schema==3 and g.saved.spent.boots==230,'shop migration retains every previous debit')
 local before=g:wallet();local rebuilt=Combat.new(data,g.saved)
 check(rebuilt:wallet()==before and rebuilt:owns('armor')and rebuilt:owns('boots'),'migration cannot charge or mint a second time')
 for i,mission in ipairs(data.missions)do
  g=fresh(i);local z=mission.sanctuary;check(z and z.radius>=1.2,'refuge exists '..mission.id)
  check(not g:is_safe(),'spawn remains outside ceasefire '..mission.id)
  check(Combat.dist(g.p,z.position)<4.8,'refuge within one second of direct walking '..mission.id)
  check(not g:blocked(z.position),'refuge centre is walkable '..mission.id)
  for k=0,7 do
   local a=k*math.pi/4;local p={z.position[1]+math.cos(a)*(z.radius-.36),z.position[2]+math.sin(a)*(z.radius-.36)}
   check(not g:blocked(p),'entire usable refuge clear of solid geometry '..mission.id..' '..k)
  end
  g:navigate(z.position);check(#g.path>0,'actual navigation reaches refuge '..mission.id)
  local distance=0;local p=g.p
  for _,q in ipairs(g.path)do distance=distance+Combat.dist(p,q);p=q end
  check(distance/data.player.speed<1.25,'reachable refuge has a short real path '..mission.id)
  quiet(g);step(g,1.25);check(g:is_safe(),'actual simulation arrives in refuge '..mission.id)
 end
 g=fresh();quiet(g);g.hp=8;g.invulnerable=0;g:hit_player();check(g.hp==7,'ordinary hit still has visible cost')
 step(g,3.95);check(g.hp==7 and not g.regenerating,'recovery waits four undamaged active seconds')
 step(g,2.1);check(g.hp==8 and g.regenerating,'time restores one health per two seconds after delay')
 g.invulnerable=0;g:hit_player();step(g,3.95);check(g.hp==7,'new damage resets recovery delay and fractional credit')
 for _,state in ipairs({'paused','background','tactical_pause'})do
  g=fresh();quiet(g);g.hp=5;g[state]=true;step(g,10)
  check(g.hp==5 and g.regen_since_hit==0,'no healing or accumulated time during '..state)
 end
 g=fresh();quiet(g);g.hp=5;g.over=true;step(g,10)
 check(g.hp==5,'defeat cannot revive itself through regeneration')
 g=fresh();quiet(g);g.p={g.m.sanctuary.position[1],g.m.sanctuary.position[2]};g.hp=5
 step(g,1);check(g.hp==7 and g.in_sanctuary and g.regenerating,'refuge restores two health per second immediately')
 step(g,10);check(g.hp==g.max_hp and not g.regenerating,'refuge recovery is capped at actual max health')
 local hp=g.hp;g.invulnerable=0;g:hit_player();check(g.hp==hp and g.damage==0,'refuge rejects direct damage attempts')
 local shots=g.shots_fired;g.cooldown=0;g:fire()
 check(g.shots_fired==shots and #g.bullets==0,'refuge cannot be used as an invulnerable firing position')
 -- Whole-body safety remains true at the usable inner edge, not outside it.
 local zone=g.m.sanctuary;g.p={zone.position[1]+zone.radius-.36,zone.position[2]}
 check(g:is_safe(),'entire player body fits at inner safe boundary')
 g.p={zone.position[1]+zone.radius-.35,zone.position[2]}
 check(not g:is_safe(),'outside the usable boundary is not falsely labelled protected')
 for angle=0,15 do
  g=fresh();quiet(g);g.walls={};local z=g.m.sanctuary
  g.p={z.position[1],z.position[2]};local a=angle*math.pi/8;local dx,dz=math.cos(a),math.sin(a)
  local b=Shots.spawn(g,{g.p[1]+dx*3,g.p[2]+dz*3},{-dx,-dz},true);b.speed=80
  Shots.update(g,.1)
  check(#g.bullets==0 and g.hp==15 and #g.fx>0,'high-speed hostile shot absorbed from direction '..angle)
 end
 check(g.sanctuary_absorbed==1,'refuge counter records actual swept absorption exactly once')
 g=fresh();quiet(g);g.walls={};local absorber=g.m.absorbers[1]
 g.p={absorber.position[1]+2,absorber.position[2]}
 local ordinary=Shots.spawn(g,{absorber.position[1]-2,absorber.position[2]},{1,0},true);ordinary.speed=80
 Shots.update(g,.1)
 check(#g.bullets==0 and g.sanctuary_absorbed==0,'ordinary absorption cannot masquerade as refuge evidence')
 g=fresh();quiet(g);g.walls={};g.p={g.m.sanctuary.position[1],g.m.sanctuary.position[2]}
 Shots.spawn(g,g.p,{1,0},true);Shots.update(g,.02)
 check(#g.bullets==0 and g.hp==15,'hostile projectile already inside refuge is neutralized')
 g=fresh();quiet(g);g.walls={};g.p={g.m.sanctuary.position[1],g.m.sanctuary.position[2]}
 Shots.spawn(g,g.p,{1,0},false);Shots.update(g,.02)
 check(#g.bullets==0,'directly spawned allied projectile cannot escape refuge')
 -- A single long frame includes reflection followed by crossing the refuge.
 g=fresh();quiet(g);g.m={sanctuary={position={0,0},radius=1.2},absorbers={}}
 g.walls={{r={-3,-2,.2,4},type='cover'}};g.p={0,0}
 local b=Shots.spawn(g,{-2,0},{-1,0},true);b.speed=80
 Shots.update(g,.1)
 check(#g.bullets==0 and g.hp==15,'reflected hostile shot cannot enter refuge within same update')
 local bounced=false;for _,fx in ipairs(g.fx)do if fx.kind=='bounce'then bounced=true end end
 check(bounced,'refuge reflection control actually bounced before absorption')
 g=funded();local lifetime=g:total();local balance=g:wallet();g.hp=3
 check(g:buy('health')and g.hp==15 and g:wallet()==balance-40,'health refill spends displayed cost and fully heals')
 check(not g:owns('health'),'refill never becomes permanently owned')
 balance=g:wallet();check(not g:buy('health')and g:wallet()==balance,'full health cannot be charged again')
 g.hp=7;check(g:buy('health')and g:wallet()==balance-40,'health remains purchasable after later damage')
 local restored=fresh(1,g.saved)
 check(restored:wallet()==g:wallet()and restored.saved.health_purchases==2,'repeated refill ledger survives reconstruction')
 check(g:total()==lifetime,'buying health never reduces lifetime stars')
 g=fresh();g.hp=3;check(not g:buy('health')and g.hp==3 and g:wallet()==0,'insufficient funds cannot heal or go into debt')
 g=funded();balance=g:wallet()
 check(not g:buy('nova2')and g:wallet()==balance,'higher weapon cannot skip predecessor')
 local row=g:shop_item('arc');check(row.locked and row.price==220 and not row.owned,'next weapon remains visible with real locked price')
 local weapon_ids={'prism','arc','nova','nova2'};local damage=0;local cooldown=1
 for _,id in ipairs(weapon_ids)do
  local item=g:shop_item(id);local old=g:wallet();check(g:buy(id),'buy weapon '..id)
  local stats=g:weapon_stats()
  check(stats.damage>=damage and stats.cooldown<=cooldown and stats.bounces==2,'weapon power rises without losing reflection '..id)
  check(g:wallet()==old-item.price and g.saved.weapon==id,'weapon price spent once and weapon equipped '..id)
  damage=stats.damage;cooldown=stats.cooldown
 end
 local previous=g:wallet();check(g:buy('prism')and g:weapon_stats().damage==1 and g:wallet()==previous,'owned weaker weapon can be equipped without payment')
 check(g:buy('nova2')and g:weapon_stats().damage==4 and g:wallet()==previous,'owned strongest weapon can be restored without payment')
 local enemy={p={2,0},hp=6,max_hp=6,shield=false};g.enemies={enemy};g.p={1,0};g.walls={};g.cooldown=0;g.aim={1,0};g:fire();Shots.update(g,.05)
 check(enemy.hp==2,'actual strongest projectile deals four damage')
 enemy.hp=6;enemy.shield=true;g:hit(enemy,0,4);check(enemy.hp==6,'strongest damage still cannot bypass reflected-shot shield')
 g=fresh();g.saved.purchases.nova2=true;g.saved.weapon='nova2'
 local task=g.bonus.tasks[1];local crystal=task.targets[1];g:hit(crystal,0,4)
 check(not task.done and crystal.hp==1,'high damage cannot bypass bonus reflection requirement')
 g=funded();local target=20
 for _,id in ipairs({'armor','armor2','armor3','armor4'})do
  local item=g:shop_item(id);local old=g:wallet();check(g:buy(id),'buy armor '..id)
  check(g.max_hp==target and g.hp==target and g:wallet()==old-item.price,'armor adds health immediately and charges exactly once '..id)
  check(not g:buy(id),'armor cannot be repurchased '..id);target=target+5
 end
 g:load(2);check(g.max_hp==35 and g.hp==35,'highest armor survives mission switch')
 restored=fresh(2,g.saved);check(restored.max_hp==35 and restored:wallet()==g:wallet(),'highest armor and balance survive reconstruction')
 g=funded();check(not g:buy('cloak2'),'second camouflage requires first tier')
 check(g:buy('cloak')and g:buy('cloak2')and g:owns('cloak2'),'camouflage tiers are actual purchases')
 check(g:buy('regen_core'),'recovery upgrade can be purchased')
 quiet(g);g.hp=5;g.regen_since_hit=0;step(g,4.1)
 check(g.hp==6,'recovery core shortens wait to two seconds')
 local catalog=g:shop_items();check(#catalog>=12,'shop has substantially more than four offerings')
 local found_health=false;for _,item in ipairs(catalog)do
  check(item.id~='boots','speed is absent from new shop')
  if item.id=='health'then found_health=item.repeatable end
 end
 check(found_health,'repeatable health remains in catalogue')
 local total_cost=0
 for _,item in ipairs(catalog)do if not item.repeatable then total_cost=total_cost+item.price end end
 check(total_cost<=4350,'all permanent upgrades are reachable within fresh campaign rewards')
 return n
end
return M
