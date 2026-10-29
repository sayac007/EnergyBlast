-- A separate explicit tactical mode. Ordinary hold/release remains aim/fire.
local Objectives=require 'main.objectives'
local Projectiles=require 'main.projectiles'
local T={range=3.5,catalogue=Objectives.catalogue}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
function T.new(g,ground)
 local c={pointer=nil}
 function c:cancel(spoken)
  local active=g.trap_ui~=nil
  self.pointer=nil;g.trap_ui=nil;g.tactical_pause=false
  if active then g.status='KURZ TIPPEN: LAUFEN · HALTEN: FEUERN' end
  if active and spoken then g.say('defold_controls')end
  if active and spoken and g.trap_test then print('DEFOLD FIELD TRAP CANCEL PASS traps='..#g.traps..' shots='..g.shots_fired)end
 end
 function c:open()
  if g.paused or g.over or g.background or g.m.kind~='trap'then return false end
  if g.trap_cooldown>0 then g.status='FALLEN LADEN: '..math.ceil(g.trap_cooldown)..' s';return false end
  if g.touch then g.touch:cancel()end
  g.path={};g.held=false;g.aiming=false;g.pending_hold=false
  g.trap_ui={mode='catalogue'};g.tactical_pause=true;self.pointer=nil
  g.status='FALLE WAEHLEN · KREUZ: ABBRECHEN';g.say('defold_trap_open')
  if g.trap_test then print('DEFOLD FIELD TRAP CATALOGUE PASS shots='..g.shots_fired)end
  return true
 end
 function c:valid(p)
  if not p or g:blocked(p)then return false,'HIER IST EINE WAND'end
  local d=distance(p,g.p)
  if d>T.range then return false,'ZU WEIT WEG'end
  if d>.001 then
   local direction={(p[1]-g.p[1])/d,(p[2]-g.p[2])/d}
   if Projectiles.ray(g.p,direction,d,g:active())then return false,'WAND DAZWISCHEN'end
  end
  return true,'TIPPE AUF FREIEN BODEN'
 end
 function c:preview(p)
  if not g.trap_ui or g.trap_ui.mode~='place'then return false end
  local valid,reason=self:valid(p)
  g.trap_ui.preview={p[1],p[2]};g.trap_ui.valid=valid;g.trap_ui.reason=reason
  return valid
 end
 function c:select(id)
  if not g.trap_ui or g.trap_ui.mode~='catalogue'or not Objectives.trap_spec(id)then return false end
  g.trap_ui.mode='place';g.trap_ui.selected=id;self.pointer=nil;self:preview(g.p)
  g.status='TIPPE AUF FREIEN BODEN IM HELLEN KREIS';g.say('defold_trap_'..id)
  if g.trap_test then print('DEFOLD FIELD TRAP SELECT PASS '..id)end
  return true
 end
 function c:place(p)
  if not self:preview(p)then return false end
  local selected=g.trap_ui.selected
  if not g:trap(p,selected)then return false end
  self:cancel(false);g.status=Objectives.trap_spec(selected).name..' BEREIT - LOCKE DEN WAECHTER';g.say('defold_trap_place')
  if g.trap_test then print('DEFOLD FIELD TRAP PLACED PASS '..selected..' shots='..g.shots_fired)end
  return true
 end
 function c:input(a)
  local ui=g.trap_ui;if not ui then return false end
  if ui.mode~='place'then return true end
  if a.pressed then
   if not self.pointer then self.pointer={id=a.id,x=a.x,y=a.y};self:preview(ground(a.x,a.y))end
  elseif self.pointer and(self.pointer.id==nil or a.id==nil or self.pointer.id==a.id)then
   self.pointer.x=a.x;self.pointer.y=a.y;self:preview(ground(a.x,a.y))
   if a.released then local p=ground(a.x,a.y);self.pointer=nil;self:place(p)end
  end
  return true
 end
 return c
end
return T
