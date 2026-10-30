-- Selection is a separate tactical gesture, never a normal move/fire contact.
local Regions=require 'main.hit_regions'
local View=require 'main.view'
local D={}
local function inside(r,x,y)
 return r and math.abs(x-r[1])<=r[3]/2 and math.abs(y-r[2])<=r[4]/2
end
function D.new(g,enemy_at,drone_at,field_at)
 local c={pointer=nil,contacts={},draining=false}
 local function restore_view()
  local previous=c.overview;if not previous then return end
  c.overview=nil
  -- A deliberate zoom while the drone is flying takes precedence over the
  -- temporary overview; selecting a drone never overwrites the saved zoom.
  if g.zoom and math.abs(g.zoom-previous.overview_zoom)<.00001 then
   g.zoom=View.zoom_factor(previous.zoom,g)
   g.camera=View.clamp_camera(g,previous.camera)
   g.zoom_focus=previous.focus
  end
 end
 local function target_overview()
  if not g.data.campaign_enabled or not g.zoom or not g.camera or not window or not window.get_size then return end
  local arena=g.arena or g.m.arena or g.data.arena
  c.overview={zoom=g.zoom,camera={g.camera[1],g.camera[2]},focus=g.zoom_focus,overview_zoom=View.minimum_zoom(g)}
  g.zoom=c.overview.overview_zoom;g.camera={arena[1]+arena[3]/2,arena[2]+arena[4]/2}
  g.zoom_focus={player={g.p[1],g.p[2]}}
 end
 enemy_at=enemy_at or function(x,y)return Regions.enemy(g,x,y)end
 local function id(a)return a.id or 0 end
 local function field(x,y)
  if field_at then return field_at(x,y)end
  if View.field then return View.field(g,x,y)end
  local L=require 'main.layout';return L.field(x,y)
 end
 local function preview(x,y)
  if drone_at then return drone_at(x,y)end
  return inside(g.drone_ui and g.drone_ui.rect,x,y)
 end
 function c:blocks_input()return self.draining or self.pointer~=nil end
 function c:reset()
  restore_view()
  self.pointer=nil;self.contacts={};self.draining=false;g:drone_cancel()
 end
 function c:cancel(spoken)
  restore_view()
  local active=g:drone_cancel()
  self.pointer=nil;self.draining=next(self.contacts)~=nil
  if active and spoken then g.say('defold_controls')end
  return active
 end
 function c:open()
  local drone=g.attack_drone
  if drone and(drone.phase=='flying'or(drone.cooldown or 0)>0)then return g:drone_open()end
  self:reset()
  if g.zoom_control then g.zoom_control:cancel()end
  return g:drone_open()
 end
 function c:select()
  self.pointer=nil
  local selected=g:drone_select()
  if selected then target_overview()end
  return selected
 end
 function c:update()
  local drone=g.attack_drone
  if c.overview and not g.drone_ui and(not drone or drone.phase=='ready'or(drone.phase=='cooldown'and(drone.cooldown or 0)<.1))then restore_view()end
 end
 function c:keep_view()
  self.overview=nil
 end
 function c:input(a)
  local key=id(a)
  if a.pressed then self.contacts[key]=true end
  if self.draining then
   if a.released then self.contacts[key]=nil end
   if not next(self.contacts)then self.draining=false;self.pointer=nil end
   return true
  end
  local ui=g.drone_ui
  if not ui then return false end
  if g.paused or g.over or g.background then self:cancel(false);return true end
  if ui.mode~='target'then
   if a.released then self.contacts[key]=nil end
   return true
  end
  if a.pressed then
   if self.pointer then return true end
   if not field(a.x,a.y)then return true end
   local enemy=enemy_at(a.x,a.y)
   if enemy and g:drone_target(enemy)then
    self.pointer={id=key};self.draining=true;return true
   end
   if preview(a.x,a.y)then
    self.pointer={id=key,x=a.x,y=a.y};ui.dragging=true;ui.x=a.x;ui.y=a.y
   end
   return true
  end
  local p=self.pointer
  if p and p.id==key then
   p.x=a.x or p.x;p.y=a.y or p.y;ui.x=p.x;ui.y=p.y
   if a.released then
    ui.dragging=false
    local enemy=field(p.x,p.y)and enemy_at(p.x,p.y)or nil
    local launched=enemy and g:drone_target(enemy)
    self.pointer=nil
    if launched then self.draining=true end
   end
  end
  if a.released then self.contacts[key]=nil end
  if self.draining and not next(self.contacts)then self.draining=false end
  return true
 end
 return c
end
return D
