-- Finite toy-drone families and bounded ground steering. No renderer allocation.
local Shots=require 'main.projectiles'
local S={max_alive=50}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
function S.alive(g)
 local count=0
 for _,e in ipairs(g.enemies or{})do if not e.optional and e.hp>0 then count=count+1 end end
 return count
end
local function outside_refuge(g,p)
 local zone=g.m.sanctuary
 return not zone or distance(zone.position,p)>zone.radius+.45
end
function S.free(g,p,origin,spacing)
 if g:blocked(p)or not outside_refuge(g,p)then return false end
 -- Rotor silhouettes have width: a newborn needs real clearance, not merely a
 -- walkable centre that lets its drawing intersect a wall at the birth frame.
 for _,offset in ipairs({{.6,0},{-.6,0},{0,.4},{0,-.4}})do
  if g:blocked({p[1]+offset[1],p[2]+offset[2]})then return false end
 end
 for _,e in ipairs(g.enemies)do if e.hp>0 and distance(e.p,p)<(spacing or .38)then return false end end
 if origin then
  local d=distance(origin,p)
  if d>.001 and Shots.ray(origin,{(p[1]-origin[1])/d,(p[2]-origin[2])/d},d,g:active())then return false end
 end
 return true
end
function S.decorate(g,e,spec)
 if not g.data.campaign_enabled then return e end
 spec=spec or{}
 g.enemy_seq=(g.enemy_seq or 0)+1;e.uid=g.enemy_seq
 e.kind=spec.kind or e.kind or'sentinel'
 e.generation=spec.generation or 0;e.max_generation=math.max(0,math.min(2,spec.max_generation or 2))
 e.replication_period=math.max(6,spec.replication_period or 8)
 e.can_replicate=(e.kind=='mini_drone'or e.kind=='splitter')and e.generation<e.max_generation and spec.can_replicate~=false
 e.replication_clock=e.replication_period+(e.uid%5)*.17
 e.replication_used=false;e.scan_period=5+(e.uid%5)*.6;e.scan_clock=e.scan_period
 e.sensor_lock=false;e.model_pending=true;e.side=e.uid%2==0 and 1 or-1
 return e
end
function S.initialize(g)
 if not g.data.campaign_enabled then return end
 g.enemy_seq=0;g.retired_enemies={}
 local kept={};local alive=0
 for _,e in ipairs(g.enemies)do
  if e.hp<=0 or e.optional or alive<S.max_alive then
   kept[#kept+1]=e;if not e.optional and e.hp>0 then alive=alive+1 end
   S.decorate(g,e,e.source_spec)
  end
 end
 g.enemies=kept;g.swarm_spawned=0;g.swarm_rejected=0
end
local function offspring(g,parent)
 if parent.replication_used or not parent.can_replicate then return 0 end
 -- Once this family has split, a later destruction cannot create it again.
 local room=S.max_alive-S.alive(g)
 if room<=0 then return 0 end
 local made=0
 for i=1,2 do if made<room then
  local position
  for attempt=0,31 do
   local angle=(attempt*math.pi/4)+(parent.uid or 0)*.47+i*math.pi
   local radius=.78+math.floor(attempt/8)*.42
   local p={parent.p[1]+math.cos(angle)*radius,parent.p[2]+math.sin(angle)*radius}
   if S.free(g,p,parent.p)then position=p;break end
  end
  if position then
   local child={p=position,hp=1,max_hp=1,kind='mini_drone',timer=.65+made*.2,warning=0,direction={1,0},burst=1,speed=1.45}
   S.decorate(g,child,{kind='mini_drone',generation=parent.generation+1,max_generation=parent.max_generation,replication_period=parent.replication_period})
   g.enemies[#g.enemies+1]=child;made=made+1;g.swarm_spawned=(g.swarm_spawned or 0)+1
   g.fx[#g.fx+1]={kind='split',p={position[1],position[2]},age=0,life=.55}
  end
 end end
 if made>0 then parent.replication_used=true end
 if made==0 then g.swarm_rejected=(g.swarm_rejected or 0)+1 end
 return made
end
function S.on_death(g,e)
 if not g.data.campaign_enabled or e.swarm_death_handled then return 0 end
 e.swarm_death_handled=true
 -- A dead parent with no capacity loses its remaining split; there is no hidden
 -- wave waiting forever to prevent mission completion.
 local made=offspring(g,e);e.replication_used=true;return made
end
local function move(g,e,dt)
 if (e.trapped or 0)>0 or e.hp<=0 or e.kind=='relay'or e.kind=='sequence'then return end
 local goal
 if e.patrol and #e.patrol>0 then goal=e.patrol[e.waypoint or 1]
 elseif e.kind=='mini_drone'or e.kind=='crawler'or e.kind=='wisp'then
  if g:is_safe()then return end
  goal=g.p
 end
 if not goal then return end
 local dx,dz=goal[1]-e.p[1],goal[2]-e.p[2];local d=math.sqrt(dx*dx+dz*dz)
 if d<.2 then if e.patrol then e.waypoint=(e.waypoint or 1)%#e.patrol+1 end;return end
 local speed=e.speed or(e.kind=='wisp'and 1.8 or e.kind=='mini_drone'and 1.45 or 1.05)
 local step=math.min(d,speed*dt);local ux,uz=dx/d,dz/d
 if e.kind=='wisp'and not e.patrol then
  local s=math.sin(g.clock*2+(e.uid or 0))*.35
  ux,uz=ux-uz*s,uz+ux*s
  local n=math.sqrt(ux*ux+uz*uz);ux,uz=ux/n,uz/n
 end
 local function allowed(p)
  if g:blocked(p)or not outside_refuge(g,p)then return false end
  -- Do not cross a thin wall in a long frame while moving toward a target.
  local nd=distance(e.p,p)
  return nd<.001 or not Shots.ray(e.p,{(p[1]-e.p[1])/nd,(p[2]-e.p[2])/nd},nd,g:active())
 end
 local trials={{e.p[1]+ux*step,e.p[2]+uz*step},{e.p[1]+ux*step,e.p[2]},{e.p[1],e.p[2]+uz*step},{e.p[1]-uz*step*e.side,e.p[2]+ux*step*e.side}}
 for _,p in ipairs(trials)do if allowed(p)then e.p=p;return end end
 e.side=-e.side
 if e.patrol then e.waypoint=(e.waypoint or 1)%#e.patrol+1 end
end
function S.update(g,dt)
 if not g.data.campaign_enabled then return end
 -- Take a snapshot: newborns begin their own timers on the next update.
 local limit=#g.enemies
 for i=1,limit do local e=g.enemies[i]
  if e.hp>0 and not e.optional then
   move(g,e,dt)
   if e.can_replicate and not e.replication_used and(e.trapped or 0)<=0 then
    e.replication_clock=e.replication_clock-dt
    if e.replication_clock<=0 then
     offspring(g,e);e.replication_clock=1
    end
   end
  end
 end
 for i=#g.enemies,1,-1 do local e=g.enemies[i]
  if e.hp<=0 and(e.death_age or 0)>1.2 then
   g.retired_enemies[#g.retired_enemies+1]=e;table.remove(g.enemies,i)
  end
 end
end
return S
