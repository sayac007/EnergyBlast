-- Active campaign data checks run against the real combat/navigation methods.
-- Scripted hits prove objective reachability/order, not a human/device victory.
local Combat=require 'main.combat'
local Objectives=require 'main.objectives'
local Shots=require 'main.projectiles'
local M={}
local function copy(p)return{p[1],p[2]}end
function M.run(data)
 if not data.campaign_enabled then return 0 end
 local n=0;local ids={};local types={};local baseline=data.missions[1].arena
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(index)
  local g=Combat.new(data);g:load(index);g.invulnerable=999
  for _,enemy in ipairs(g.enemies)do enemy.timer=999;enemy.warning=0;enemy.patrol=nil end
  return g
 end
 check(#data.missions==16,'six existing missions plus exactly ten new missions')
 check(data.max_hostiles==50,'explicit fifty-hostile population limit')
 local first={'reactor','citadel','dock','forge','echo','rescue'}
 for i,id in ipairs(first)do check(data.missions[i].id==id,'existing saved mission identity retained '..id)end
 local old_score=0
 for _,m in ipairs(data.missions)do
  if m.complexity<=6 then
   for _,prefix in ipairs({'mission:','skill:','secret:','bonus:prism:','bonus:pattern:'})do old_score=old_score+(data.rewards[prefix..m.id]or 0)end
  end
 end
 check(old_score==4350,'all old earned reward amounts remain available to save migration')
 for index,m in ipairs(data.missions)do
  local g=fresh(index);local arena=m.arena;local safe=m.sanctuary
  check(not ids[m.id],'unique mission id '..m.id);ids[m.id]=true
  check(m.complexity==index,'campaign complexity advances explicitly '..m.id)
  check(arena and arena[3]>0 and arena[4]>0 and g.arena==arena,'mission-specific arena consumed by simulation '..m.id)
  if index>6 then check(arena[3]>=baseline[3]*1.5 and arena[4]>=baseline[4]*1.5,'advanced arena at least fifty percent larger on both axes '..m.id)end
  if index>7 then
   local before=data.missions[index-1].arena
   check(arena[3]>=before[3]and arena[4]>=before[4],'later advanced fields never shrink '..m.id)
  end
  check(m.spawn[1]==safe.position[1]and m.spawn[2]==safe.position[2]and g:is_safe(),'Zikkurat is the actual safe mission start '..m.id)
  check(not g:blocked(g.p),'safe starting point is real free floor '..m.id)
  for j=0,7 do
   local a=j*math.pi/4;local p={g.p[1]+math.cos(a)*(safe.radius-.36),g.p[2]+math.sin(a)*(safe.radius-.36)}
   check(not g:blocked(p),'whole usable refuge fits free floor '..m.id..' '..j)
  end
  check(not m.bonuses and not m.secret and not m.escort,'no hidden bonus/chest/escort objective '..m.id)
  check(g.bonus.total==0 and #g.bonus.tasks==0,'no live optional bonus task loaded '..m.id)
  check(g:mission_state().treasures_remaining==0 and g:mission_state().bonus_total==0,'objective counters contain no removed treasure hunt '..m.id)
  check(m.attack_drone and m.attack_drone.stock>=3 and m.attack_drone.stock<=8,'explicit finite drone stock '..m.id)
  -- Gated arenas deliberately expose their far side only during the open phase.
  g.clock=5
  local enemies={};for _,enemy in ipairs(g.enemies)do enemies[#enemies+1]=enemy end
  check(#enemies>0 and #enemies<=50,'initial hostile/objective population bounded '..m.id)
  for _,enemy in ipairs(enemies)do
   types[enemy.kind or'sentinel']=true
   check(not enemy.optional and enemy.hp>0,'actual active enemy or signal objective '..m.id)
   check(not g:blocked(enemy.p),'target on free floor '..m.id)
   g:navigate(enemy.p)
   check(#g.path>0 and Combat.dist(g.path[#g.path],enemy.p)<.5,'actual movement graph reaches target '..m.id)
   local dx,dz=g.p[1]-enemy.p[1],g.p[2]-enemy.p[2];local d=math.sqrt(dx*dx+dz*dz)
   check(Shots.ray(enemy.p,{dx/d,dz/d},d-.03,g:active())~=nil,'initial hostile line to refuge meets actual solid cover '..m.id)
  end
  for _,spec in ipairs(m.turrets)do for _,point in ipairs(spec.patrol or{})do check(not g:blocked(point),'patrol waypoints remain on free floor '..m.id)end end
  -- The dogleg shelter has a genuine navigable exit, not an enclosed start cell.
  local start=copy(g.p);local exit={start[1]+4.2,start[2]-.5}
  g:navigate(exit)
  check(#g.path>0 and Combat.dist(g.path[#g.path],exit)<.5,'actual path leaves protected dogleg shelter '..m.id)
  g.clock=5;g:navigate(m.goal)
  check(#g.path>0 and Combat.dist(g.path[#g.path],m.goal)<.5,'actual route reaches final objective with live gate open '..m.id)
  g.path={};local hp=g.hp;g.invulnerable=0
  for _,enemy in ipairs(enemies)do
   local dx,dz=g.p[1]-enemy.p[1],g.p[2]-enemy.p[2]
   local shot=Shots.spawn(g,enemy.p,{dx,dz},true);shot.speed=120
   Shots.update(g,.5)
  end
  check(g.hp==hp and g.damage==0 and g:is_safe(),'real swept hostile shots cannot hurt the mission start '..m.id)
  -- Drive real objective methods in the correct order. No HP/solved flag is
  -- assigned by the test; this also catches locked bosses and signal softlocks.
  g=fresh(index)
  for _,enemy in ipairs(g.enemies)do if enemy.kind=='relay'then g:hit(enemy,1,100)end end
  local budget=0
  while not g.solved do
   local target
   for _,enemy in ipairs(g.enemies)do if enemy.hp>0 and enemy.kind~='sequence'then target=enemy;break end end
   if not target then break end
   budget=budget+1;assert(budget<400,'bounded objective completion '..m.id)
   if target.trap_shield and(target.trapped or 0)<=0 then
    g.p=copy(target.p);g.trap_cooldown=0
    check(g:trap(target.p,'magnet'),'actual trap can be prepared at reachable guardian '..m.id)
    Objectives.update(g,.01,Combat.dist)
    check((target.trapped or 0)>0,'real trap opens guardian shield '..m.id)
   end
   g:hit(target,1,100)
  end
  if m.sequence then
   for _,order in ipairs(m.sequence)do
    for _,enemy in ipairs(g.enemies)do if enemy.kind=='sequence'and enemy.order==order then g:hit(enemy,0);break end end
   end
  end
  if not g.solved and m.exit_required then
   g.p=copy(m.goal);g.clock=5;g:update(.025)
  end
  check(g.solved and g.saved.earned['mission:'..m.id]==true,'real objective path can finish campaign mission '..m.id)
  local before=g:total();g:load(index)
  check(g:total()==before and g:award('mission:'..m.id)==0,'reloading completed mission cannot mint another reward '..m.id)
 end
 for _,kind in ipairs({'mini_drone','splitter','crawler','wisp'})do check(types[kind],'campaign contains distinct '..kind..' enemies')end
 return n
end
return M
