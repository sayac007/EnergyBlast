-- One decision only: elapsed press time. No enemy/wall hit-test or drag shortcut.
local M={}
local Traps=require 'main.trap_controls'
function M.new(g,ground)
 local c={pointer=nil,threshold=g.data.hold_seconds or .3}
 g.trap_control=Traps.new(g,ground)
 function c:cancel()
  self.pointer=nil;g.aiming=false;g.pending_hold=false;g.hold_progress=0;g.held=false
  g.trap_control:cancel(false)
 end
 function c:aim()
  local p=self.pointer;if not p then return end
  local q=ground(p.x,p.y);g.target=q
  local dx,dy=q[1]-g.p[1],q[2]-g.p[2];local length=math.sqrt(dx*dx+dy*dy)
  if length>.05 then g.aim={dx/length,dy/length}end
  g.aiming=true;g.pending_hold=false;g.path={};g.status='ZIELEN - Loslassen: Schuss'
 end
 function c:update(dt)
  if not self.pointer then return end
  if g.paused or g.over or g.background then self:cancel();return end
  self.pointer.seconds=self.pointer.seconds+dt
  g.hold_progress=math.min(1,self.pointer.seconds/self.threshold)
  if self.pointer.seconds+1e-7>=self.threshold then self:aim()end
 end
 function c:input(a)
  if g.trap_ui then return g.trap_control:input(a)end
  if g.paused or g.over or g.background then return end
  if a.pressed then
   if self.pointer then return end
   self.pointer={id=a.id,x=a.x,y=a.y,seconds=0};g.path={};g.aiming=false;g.pending_hold=true;g.hold_progress=0
  elseif self.pointer and(self.pointer.id==nil or a.id==nil or self.pointer.id==a.id)then
   self.pointer.x=a.x;self.pointer.y=a.y
   if self.pointer.seconds+1e-7>=self.threshold then self:aim()end
   if a.released then
    if g.aiming then g:fire();g.status='SCHUSS - KURZ TIPPEN: LAUFEN';if g.ui_test then print('DEFOLD UI LONG HOLD shots='..g.shots_fired)end else g.target=ground(a.x,a.y);g:navigate(g.target);g.status='LAUFEN - Halten: Zielen';if g.ui_test then print('DEFOLD UI SHORT TAP shots='..g.shots_fired)end end
    self.pointer=nil;g.aiming=false;g.pending_hold=false;g.hold_progress=0
   end
  end
 end
 return c
end
return M
