-- Scene zoom owns two field fingers before either can become a second shot.
-- HUD geometry stays fixed; rendering and world hit tests use View's same zoom.
local View=require 'main.view'
local Layout=require 'main.layout'
local Z={}
local function distance(a,b)return math.sqrt((a.x-b.x)^2+(a.y-b.y)^2)end
local function point(a,b)return(a.x+b.x)/2,(a.y+b.y)/2 end
local function eligible(g,a)
 return not g.dialog and not g.paused and not g.over and not g.background and not g.tactical_pause and Layout.field(a.x,a.y)
end
function Z.new(g)
 local c={g=g,contacts={},pinch=nil,draining=false,dirty=false}
 g.zoom=View.zoom_factor(g.saved and g.saved.zoom)
 if g.saved and g.saved.zoom~=nil then g.saved.zoom=g.zoom end
 local function stop_actions()
  if g.touch then g.touch:cancel()end
  g.path={};g.held=false;g.aiming=false;g.dragging=false;g.pending_hold=false;g.hold_progress=0
 end
 function c:save()
  if not self.dirty then return end
  self.dirty=false;g.saved.zoom=g.zoom;if g.changed then g.changed()end
 end
 function c:set(value,x,y,save)
  local zoom=View.zoom_factor(value)
  if math.abs(zoom-g.zoom)<.000001 then return false end
  x=x or(Layout.left+Layout.right)/2;y=y or(Layout.bottom+Layout.top)/2
  local before=View.unproject(g,x,y)
  g.zoom=zoom
  local after=View.unproject(g,x,y)
  local camera=g.camera or{0,0}
  g.camera=View.clamp_camera(g,{camera[1]+before[1]-after[1],camera[2]+before[2]-after[2]})
  g.zoom_focus={player={g.p[1],g.p[2]}}
  self.dirty=true
  if save~=false then self:save()end
  return true
 end
 function c:step(direction)
  if g.dialog or g.paused or g.background or g.tactical_pause then return false end
  stop_actions();return self:set(g.zoom+(direction>0 and .15 or-.15))
 end
 function c:cancel()
  self:save();self.contacts={};self.pinch=nil;self.draining=false;g.zooming=false
 end
 function c:blocks_mouse()
  return self.draining or self.pinch~=nil or next(self.contacts)~=nil
 end
 function c:input(packet)
  -- Scan the complete event packet before forwarding any ordinary gesture.
  -- A contact is eligible only if it STARTED on the live floor, never on HUD.
  local released={}
  for _,a in ipairs(packet)do
   local id=a.id
   if id~=nil then
    local p=self.contacts[id]
    if a.pressed then p={x=a.x,y=a.y,field=eligible(g,a)};self.contacts[id]=p
    elseif p then p.x=a.x or p.x;p.y=a.y or p.y end
    if a.released then released[id]=true end
   end
  end
  local pair={};local active=0
  for id,p in pairs(self.contacts)do if not released[id]then
   active=active+1
   if p.field and Layout.field(p.x,p.y)then pair[#pair+1]={id=id,x=p.x,y=p.y}end
  end end
  table.sort(pair,function(a,b)return tostring(a.id)<tostring(b.id)end)
  local consumed=self.draining or self.pinch~=nil
  if #pair>=2 and not g.dialog and not g.paused and not g.over and not g.background and not g.tactical_pause then
   consumed=true;self.draining=true;g.zooming=true
   local a,b=pair[1],pair[2];local x,y=point(a,b)
   if not self.pinch or self.pinch.a~=a.id or self.pinch.b~=b.id then
    stop_actions();self.pinch={a=a.id,b=b.id,distance=math.max(24,distance(a,b)),zoom=g.zoom}
   else
    self:set(self.pinch.zoom*math.max(24,distance(a,b))/self.pinch.distance,x,y,false)
   end
  elseif self.pinch then
   -- One remaining finger cannot turn the tail of a pinch into movement/fire.
   self.pinch=nil;g.zooming=false;stop_actions();self:save()
  end
  for id in pairs(released)do self.contacts[id]=nil end
  if active==0 then
   self.pinch=nil;self.draining=false;g.zooming=false;self:save()
  end
  return consumed
 end
 return c
end
return Z
