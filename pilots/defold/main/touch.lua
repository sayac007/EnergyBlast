-- Current direct touch gestures; historical fixtures retain their old controls.
local Legacy=require 'main.touch_legacy'
local Regions=require 'main.hit_regions'
local Traps=require 'main.trap_controls'
local M={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
function M.new(g,ground)
 if g.data.controls~='direct_touch_hold_fire_drag_hero'then return Legacy.new(g,ground)end
 local c={pointer=nil,pending_shot=nil,threshold=g.data.hold_seconds or .14}
 g.trap_control=Traps.new(g,ground)
 local function log(message)if g.direct_touch_test or g.ui_test then print('DEFOLD DIRECT '..message)end end
 function c:cancel()
  if g.dragging then g.path={}end
  self.pointer=nil;self.pending_shot=nil;g.aiming=false;g.pending_hold=false;g.hold_progress=0;g.held=false;g.dragging=false
  g.trap_control:cancel(false)
 end
 local function aim_point(q)
  g.target={q[1],q[2]};local dx,dy=q[1]-g.p[1],q[2]-g.p[2]
  local length=math.sqrt(dx*dx+dy*dy)
  if length>.03 then g.aim={dx/length,dy/length}end
 end
 function c:aim()
  local p=self.pointer;if not p then return end
  local enemy=p.enemy
  if enemy and enemy.hp<=0 then enemy=nil;p.enemy=nil end
  local q=enemy and enemy.p or ground(p.x,p.y)
  aim_point(q)
  g.aiming=true;g.pending_hold=false;g.held=true;g.path={}
  g.status='FEUERN - FINGER BEWEGEN: ZIELEN'
 end
 function c:fire_mode(enemy)
  self.pointer.mode='fire';self.pointer.enemy=enemy;self:aim()
  local before=g.shots_fired;g:fire()
  if enemy and before==g.shots_fired then self.pending_shot={enemy=enemy,ttl=(g.data.combat.fire_cooldown or .24)+.08,before=before};log('BUFFERED PRESS shots='..before)end
  log((enemy and'ENEMY PRESS'or'GROUND HOLD')..' shots='..g.shots_fired..' elapsed='..string.format('%.3f',self.pointer.seconds)..' emitted='..tostring(g.shots_fired>before))
  if enemy then log('ENEMY AIM target_x='..g.target[1]..' target_z='..g.target[2])end
 end
 function c:drag()
  local p=self.pointer;if not p or p.mode~='drag'then return end
  local dx,dy=p.x-p.start_x,p.y-p.start_y
  if not p.moved and dx*dx+dy*dy<36 then return end
  p.moved=true
  local q=ground(p.x,p.y)
  local target={p.anchor[1]+q[1]-p.origin[1],p.anchor[2]+q[2]-p.origin[2]}
  if p.drag_clock>0 or(p.last_target and distance(p.last_target,target)<.12)then return end
  p.drag_clock=.08;p.last_target=target;g.target=target;g:navigate(target)
  g.status='FIGUR ZIEHEN: LAUFEN'
  if not p.drag_logged then p.drag_logged=true;log('HERO DRAG shots='..g.shots_fired)end
 end
 function c:update(dt)
  if g.direct_touch_test and not self.fixture_logged and g.project and not g.paused then
   local hx,hy=g.project(g,g.p,1.75);local tx,ty=g.project(g,{g.p[1]-2,g.p[2]+1},0);local ax,ay=g.project(g,{g.p[1]+1,g.p[2]-2},0)
   local e=nil;for _,candidate in ipairs(g.enemies)do if candidate.hp>0 and not candidate.optional then e=candidate;break end end
   if e then local r=Regions.bounds(g,e);self.fixture_logged=true;log('READY '..math.floor(hx)..' '..math.floor(hy)..' '..math.floor(tx)..' '..math.floor(ty)..' '..math.floor(ax)..' '..math.floor(ay)..' '..math.floor(r.x+r.w/2-3)..' '..math.floor(r.y))end
  end
  if(g.direct_touch_test or g.ui_test)and self.test_last_shots~=g.shots_fired then self.test_last_shots=g.shots_fired;log('COUNT shots='..g.shots_fired..' held='..tostring(g.held)..' mode='..(self.pointer and self.pointer.mode or'none'))end
  if self.tap_anchor and distance(g.p,self.tap_anchor)>.15 then log('GROUND MOVED shots='..g.shots_fired);self.tap_anchor=nil end
  if g.paused or g.over or g.background then if self.pointer or self.pending_shot then self:cancel()end;return end
  local queued=self.pending_shot
  if queued then
   queued.ttl=queued.ttl-dt
   if queued.enemy.hp<=0 or queued.ttl<0 or g.shots_fired>queued.before then self.pending_shot=nil
   elseif g.cooldown<=0 then
    aim_point(queued.enemy.p);g:fire();self.pending_shot=nil;log('BUFFERED SHOT shots='..g.shots_fired)
   end
  end
  local p=self.pointer;if not p then return end
  p.seconds=p.seconds+dt
  if p.mode=='drag'then
   p.drag_clock=math.max(0,p.drag_clock-dt);self:drag()
   if not p.move_logged and distance(g.p,p.anchor)>.15 then p.move_logged=true;log('HERO MOVED shots='..g.shots_fired..' distance='..string.format('%.2f',distance(g.p,p.anchor)))end
   return
  end
  g.hold_progress=math.min(1,p.seconds/self.threshold)
  if p.mode=='ground'and p.seconds+1e-7>=self.threshold then self:fire_mode(nil)
  elseif p.mode=='fire'then self:aim()end
 end
 function c:input(a)
  if g.trap_ui then return g.trap_control:input(a)end
  if g.paused or g.over or g.background then if self.pointer then self:cancel()end;return end
  if a.pressed then
   if self.pointer then return end
   self.pending_shot=nil
   self.tap_anchor=nil
   local p={id=a.id,x=a.x,y=a.y,start_x=a.x,start_y=a.y,seconds=0,mode='ground'}
   self.pointer=p;g.path={};g.aiming=false;g.pending_hold=false;g.hold_progress=0;g.held=false
   local enemy=Regions.enemy(g,a.x,a.y);local own=Regions.own(g,a.x,a.y)
   if own and enemy then
    local hr,er=Regions.hero(g),Regions.bounds(g,enemy)
    own=(a.x-hr.x)^2+(a.y-hr.y)^2<=(a.x-er.x)^2+(a.y-er.y)^2
   end
   if own then
    p.mode='drag';p.origin=ground(a.x,a.y);p.anchor={g.p[1],g.p[2]};p.drag_clock=0;g.dragging=true
    log('HERO PRESS shots='..g.shots_fired)
   else
    if enemy then self:fire_mode(enemy)else g.pending_hold=true end
   end
   return
  end
  local p=self.pointer
  if not p or not(p.id==nil or a.id==nil or p.id==a.id)then return end
  p.x=a.x;p.y=a.y
  if p.mode=='drag'then self:drag()
  elseif p.mode=='fire'then
   if p.enemy then local r=Regions.bounds(g,p.enemy);if math.abs(p.x-r.x)>r.w/2 or math.abs(p.y-r.y)>r.h/2 then p.enemy=nil end end
   self:aim()
  end
  if a.released then
   if p.mode=='ground'then
    g.target=ground(a.x,a.y);g:navigate(g.target);self.tap_anchor={g.p[1],g.p[2]};g.status='LAUFEN - HALTEN: FEUERN';log('GROUND TAP shots='..g.shots_fired)
   elseif p.mode=='drag'then g.path={};log('HERO RELEASE shots='..g.shots_fired)
   else log('FIRE RELEASE shots='..g.shots_fired)end
   self.pointer=nil;g.aiming=false;g.pending_hold=false;g.hold_progress=0;g.held=false;g.dragging=false
  end
 end
 return c
end
return M
