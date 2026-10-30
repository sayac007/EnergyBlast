-- A finite stock of explicitly launched toy attack drones. Flight and impacts
-- use the live arena; no renderer or input handler can grant a kill directly.
local Shots=require 'main.projectiles'
local A={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function copy(p)return{p[1],p[2]}end
local function clear(g,a,b)
 local d=distance(a,b)
 return d<.001 or not Shots.ray(a,{(b[1]-a[1])/d,(b[2]-a[2])/d},d,g:active())
end
local function live_target(g,e)
 if type(e)~='table'or type(e.hp)~='number'or e.hp<=0 or e.optional or e.kind=='sequence'then return false end
 for _,candidate in ipairs(g.enemies)do if candidate==e then return true end end
 return false
end
local function route(g,origin,target)
 if g:blocked(target)then return nil end
 if clear(g,origin,target)then return{copy(target)}end
 -- Reuse the exact movement graph without changing the hero or their route.
 local hero,path=g.p,g.path
 g.p=copy(origin);g.path={}
 local ok,err=pcall(g.navigate,g,target)
 local planned=g.path
 g.p=hero;g.path=path
 if not ok then return nil,err end
 if #planned==0 or distance(planned[#planned],target)>.8 then return nil end
 local result={}
 for _,p in ipairs(planned)do result[#result+1]=copy(p)end
 return result
end
local function release_selection(g)
 local was_open=g.drone_ui~=nil
 g.drone_ui=nil
 if was_open then g.tactical_pause=false end
end
local function reset_ready(g,status,refund)
 local d=g.attack_drone
 if not d then return end
 if refund then d.stock=math.min(d.max_stock,d.stock+1)end
 d.phase='cooldown';d.cooldown=1;d.target=nil;d.path={};d.failed=true
 if status then g.status=status end
end
function A.bind(g)
 function g:drone_state()
  return self.attack_drone or{enabled=false,stock=0,max_stock=0,phase='ready',p=copy(self.p or{0,0}),path={}}
 end
 function g:drone_cancel()
  local d=self.attack_drone;local active=self.drone_ui~=nil
  release_selection(self)
  if d and d.phase=='select'then d.phase='ready' end
  if active then self.status='DROHNENWAHL BEENDET - KURZ TIPPEN: LAUFEN'end
  return active
 end
 function g:drone_open()
  local d=self.attack_drone
  if not d or not d.enabled or self.paused or self.over or self.background then return false end
  if d.phase=='flying'or(d.cooldown or 0)>0 then self.status='DROHNE IST NOCH UNTERWEGS';return false end
  if d.stock<=0 then self.status='KEINE DROHNEN MEHR - WAFFE ODER FALLE NUTZEN';self.say('defold_drone_empty');return false end
  if self.touch then self.touch:cancel()end
  if self.trap_control then self.trap_control:cancel(false)end
  self.trap_ui=nil;self.path={};self.held=false;self.aiming=false;self.pending_hold=false;self.dragging=false
  d.phase='select';d.p=copy(self.p);d.failed=false
  self.drone_ui={mode='catalogue'};self.tactical_pause=true
  self.status='DROHNE AUS DEM VORRAT WAEHLEN';self.say('defold_drone_open')
  return true
 end
 function g:drone_select()
  if not self.drone_ui or self.drone_ui.mode~='catalogue'or self.paused or self.over or self.background then return false end
  self.drone_ui.mode='target';self.status='WAEHLE DAS ZIEL - GEGNER ANTIPPEN ODER DROHNE ZIEHEN'
  self.say('defold_drone_target');return true
 end
 function g:drone_target(enemy)
  local d=self.attack_drone
  if not d or not d.enabled or not self.drone_ui or self.drone_ui.mode~='target'or self.paused or self.over or self.background or d.stock<=0 then return false end
  if not live_target(self,enemy)then self.status='WAEHLE EINEN LEBENDEN GEGNER';return false end
  if self:locked(enemy)then self.status='ERST DIE RELAIS AUSSCHALTEN';self.say('raid_relays');return false end
  local planned=route(self,self.p,enemy.p)
  if not planned then self.status='KEIN FREIER FLUGWEG - ANDERES ZIEL WAEHLEN';return false end
  self.path={};self.held=false;self.aiming=false;self.pending_hold=false;self.dragging=false
  d.stock=d.stock-1;d.phase='flying';d.p=copy(self.p);d.target=enemy;d.path=planned;d.age=0;d.replan=.6;d.last_target=copy(enemy.p);d.failed=false
  d.launched=(d.launched or 0)+1
  release_selection(self)
  self.status='DROHNE UNTERWEGS - VORRAT '..d.stock;self.say('defold_drone_launch')
  return true
 end
end
function A.reset(g)
 local cfg=g.m.attack_drone
 local stock=cfg and math.max(0,math.min(12,math.floor(tonumber(cfg.stock)or 3)))or 0
 local arena=g.arena or g.m.arena or g.data.arena
 local speed=cfg and math.max(3,math.min(12,tonumber(cfg.speed)or 7))or 7
 g.attack_drone={enabled=cfg~=nil,stock=stock,max_stock=stock,phase='ready',p=copy(g.p),path={},age=0,cooldown=0,
  speed=speed,timeout=math.min(40,math.max(12,(arena[3]+arena[4])/speed*2+4)),launched=0,kills=0}
 release_selection(g)
end
local function impact(g,d)
 local enemy=d.target
 if not live_target(g,enemy)then reset_ready(g,'ZIEL SCHON BESIEGT - DROHNE ZURUECK',true);return end
 if g:locked(enemy)then reset_ready(g,'RELAIS SCHUETZEN DAS ZIEL - DROHNE ZURUECK',true);return end
 local p=copy(enemy.p)
 g.fx[#g.fx+1]={kind='lightning',primary=true,p=p,a=copy(d.p),b=p,age=0,life=.75}
 -- Electronic disruption is local and cannot propagate through solid cover.
 for _,other in ipairs(g.enemies)do
  if other~=enemy and other.hp>0 and not other.optional and other.kind~='sequence'and other.kind~='relay'and distance(other.p,p)<2.5 and clear(g,p,other.p)then
   other.trapped=math.max(other.trapped or 0,3)
   g.fx[#g.fx+1]={kind='lightning',p=copy(other.p),a=p,b=copy(other.p),age=0,life=.5}
  end
 end
 -- The ordinary hit path owns splits, mission completion, animation and stars.
 -- Only this committed contact impact suppresses the target's ordinary shield;
 -- a boss's relay lock was checked above and is never bypassed.
 local shield,trapped=enemy.shield,enemy.trapped
 enemy.shield=false;enemy.trapped=math.max(enemy.trapped or 0,1.5)
 g:hit(enemy,1,math.max(1,enemy.hp))
 enemy.shield=shield;enemy.trapped=trapped
 if enemy.hp<=0 then d.kills=d.kills+1 end
 d.phase='cooldown';d.cooldown=2;d.target=nil;d.path={};d.age=0
 if not g.solved then g.status='DROHNENTREFFER - VORRAT '..d.stock end
end
function A.update(g,dt)
 local d=g.attack_drone
 if not d or not d.enabled or g.paused or g.over or g.background or g.tactical_pause then return end
 dt=math.max(0,math.min(.05,dt))
 if d.phase=='cooldown'then
  d.cooldown=math.max(0,d.cooldown-dt)
  if d.cooldown==0 then d.phase='ready';d.p=copy(g.p)end
  return
 end
 if d.phase~='flying'then d.p=copy(g.p);return end
 d.age=d.age+dt;d.replan=d.replan-dt
 if d.age>d.timeout then reset_ready(g,'FLUGWEG BLOCKIERT - DROHNE ZURUECK',true);return end
 if not live_target(g,d.target)then reset_ready(g,'ZIEL SCHON BESIEGT - DROHNE ZURUECK',true);return end
 local target=d.target
 if distance(d.p,target.p)<=.8 and clear(g,d.p,target.p)then impact(g,d);return end
 if d.replan<=0 and(distance(target.p,d.last_target)>.6 or #d.path==0)then
  local planned=route(g,d.p,target.p)
  if planned then d.path=planned;d.last_target=copy(target.p)end
  d.replan=.6
 end
 while #d.path>0 and distance(d.p,d.path[1])<.06 do table.remove(d.path,1)end
 local next_point=d.path[1]
 if not next_point then d.replan=0;return end
 local length=distance(d.p,next_point);local step=math.min(length,d.speed*dt)
 local next_p={d.p[1]+(next_point[1]-d.p[1])/length*step,d.p[2]+(next_point[2]-d.p[2])/length*step}
 if g:blocked(next_p)or not clear(g,d.p,next_p)then
  local planned=route(g,d.p,target.p)
  if planned then d.path=planned;d.last_target=copy(target.p)end
  d.replan=.6;return
 end
 d.p=next_p
 if length<=step+.001 then table.remove(d.path,1)end
end
return A
