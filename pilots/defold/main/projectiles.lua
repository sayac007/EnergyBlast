-- Swept live collisions: every solid surface in current Defold arenas reflects.
-- No renderer calls this module to display a predicted route.
local P={}
local EPS=.0001
local function normal(axis,sign)local n={0,0};n[axis]=sign;return n end
local function merge(a,b)return{a[1]~=0 and a[1]or b[1],a[2]~=0 and a[2]or b[2]}end
function P.ray(o,d,length,walls)
 local best=nil
 for _,wall in ipairs(walls)do
  local r=wall.r;local enter,leave=-math.huge,math.huge;local en,ex={0,0},{0,0};local valid=true
  for axis=1,2 do
   local lo,hi=r[axis],r[axis]+r[axis+2]
   if math.abs(d[axis])<1e-9 then
    if o[axis]<lo or o[axis]>hi then valid=false;break end
   else
    local a,b=(lo-o[axis])/d[axis],(hi-o[axis])/d[axis]
    local sign=d[axis]>0 and -1 or 1
    if a>b then a,b=b,a end
    local na,nb=normal(axis,sign),normal(axis,-sign)
    if a>enter+1e-7 then enter=a;en=na elseif math.abs(a-enter)<1e-7 then en=merge(en,na)end
    if b<leave-1e-7 then leave=b;ex=nb elseif math.abs(b-leave)<1e-7 then ex=merge(ex,nb)end
    if enter>leave+1e-7 then valid=false;break end
   end
  end
  if valid then
   local t,n=enter,en;if t<1e-7 then t,n=leave,ex end
   if t>=1e-7 and t<=length+1e-7 then
    if not best or t<best.t-1e-7 then best={t=t,n=n,type=wall.type,p={o[1]+d[1]*t,o[2]+d[2]*t}}
    elseif math.abs(t-best.t)<1e-7 then best.n=merge(best.n,n)end
   end
  end
 end
 return best
end
local function circle_hit(o,d,length,p,radius)
 local x,y=o[1]-p[1],o[2]-p[2];local c=x*x+y*y-radius*radius
 if c<=0 then return 0 end
 local b=x*d[1]+y*d[2];local discriminant=b*b-c
 if discriminant<0 then return nil end
 local t=-b-math.sqrt(discriminant)
 if t>=0 and t<=length then return t end
 return nil
end
function P.spawn(g,origin,direction,enemy)
 local n=math.sqrt(direction[1]^2+direction[2]^2);if n<1e-9 then return nil end
 local cfg=g.data.combat
 local budget=enemy and(cfg.enemy_bounces or 0)or(g:total()>=100 and g.saved.weapon=='prism'and 2 or 1)
 local b={p={origin[1],origin[2]},direction={direction[1]/n,direction[2]/n},enemy=enemy,
  age=0,alpha=1,lifetime=enemy and(cfg.enemy_seconds or 6)or(cfg.player_seconds or 3),bounces=0,max_bounces=budget,segment=1,remaining=enemy and(cfg.enemy_range or 20)or(cfg.shot_range or 28),
  speed=enemy and cfg.enemy_bullet_speed or cfg.player_bullet_speed}
 g.bullets[#g.bullets+1]=b;return b
end
function P.update(g,dt)
 local walls=g:active()
 for i=#g.bullets,1,-1 do
  local b=g.bullets[i];local elapsed=math.max(0,math.min(dt,b.lifetime-b.age));b.age=b.age+elapsed;b.alpha=math.min(1,math.max(0,(b.lifetime-b.age)/.35));local distance=math.min(b.speed*elapsed,b.remaining);local removed=false
  -- Each iteration spends distance or a reflection. Bound coincident corner hits.
  for iteration=1,b.max_bounces+2 do
   if distance<=1e-7 or removed then break end
   local wall=P.ray(b.p,b.direction,distance,walls);local travel=wall and math.min(wall.t,distance)or distance
   local target=nil;local target_t=travel+1e-7
   if b.enemy then
    local t=circle_hit(b.p,b.direction,travel,g.p,.36);if t then target_t=t;target='player'end
   else
    local radius=(g.saved.earned['secret:bank']or g.saved.earned['secret:reactor'])and .56 or .48
    for _,e in ipairs(g.enemies)do if e.hp>0 then
     local t=circle_hit(b.p,b.direction,travel,e.p,radius)
     if t and t<target_t then target_t=t;target=e end
    end end
   end
   for _,zone in ipairs(g.m.absorbers or{})do
    local t=circle_hit(b.p,b.direction,travel,zone.position,zone.radius)
    if t and t<=target_t then target_t=t;target='absorber'end
   end
   if target then travel=target_t end
   b.p={b.p[1]+b.direction[1]*travel,b.p[2]+b.direction[2]*travel};b.remaining=b.remaining-travel;distance=distance-travel
   if target then
    if target=='absorber'then g.fx[#g.fx+1]={kind='absorb',p={b.p[1],b.p[2]},age=0,life=.22}elseif target=='player'then g:hit_player()else g:hit(target,b.bounces)end;removed=true
   elseif wall then
    local reflective=g.data.combat.reflect_all_walls or wall.type=='reflector'
    if reflective and b.bounces<b.max_bounces then
     -- A face flips one component; an exact joined corner flips both.
     for axis=1,2 do if wall.n[axis]~=0 then b.direction[axis]=-b.direction[axis]end end
     b.bounces=b.bounces+1;b.segment=b.bounces+1
     g.fx[#g.fx+1]={kind='bounce',p={b.p[1],b.p[2]},age=0,life=.16}
     if g.sfx then g.sfx('bounce')end
     local gap=math.min(EPS,b.remaining)
     b.p={b.p[1]+b.direction[1]*gap,b.p[2]+b.direction[2]*gap};b.remaining=b.remaining-gap;distance=math.max(0,distance-gap)
    else g.fx[#g.fx+1]={kind='dissipate',p={b.p[1],b.p[2]},age=0,life=.18};removed=true end
   else break end
  end
  b.alpha=math.min(1,math.max(0,math.min(b.lifetime-b.age,b.remaining/b.speed)/.35))
  if not removed and(b.remaining<=EPS or b.age>=b.lifetime)then g.fx[#g.fx+1]={kind='dissipate',p={b.p[1],b.p[2]},age=0,life=.18};removed=true end
  if removed then table.remove(g.bullets,i)end
 end
end
return P
