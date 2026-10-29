-- Explicit native-test fixture. Production missions never call these overrides.
local View=require 'main.view'
local Regions=require 'main.hit_regions'
local Shots=require 'main.projectiles'
local F={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function clear(g,a,b)
 local d=distance(a,b)
 return not Shots.ray(a,{(b[1]-a[1])/d,(b[2]-a[2])/d},d-.03,g:active())
end
local function free_floor_target(g,x,y)
 if Regions.own(g,x,y)or Regions.enemy(g,x,y)then return false end
 if g.m.kind=='trap'then
  local px,py=View.project(g,g.p,.4)
  local bx=math.max(198,math.min(1082,px+87));local by=math.max(154,math.min(566,py+20))
  if math.abs(x-bx)<=46 and math.abs(y-by)<=46 then return false end
 end
 return true
end
function F.init(self)
 if sys.get_config_string('project.polish_ui_test','0')~='1'then return end
 self.polish_ui_test=true;self.g.polish_ui_test=true;self.muted=true
 local g=self.g
 g.saved={earned={},clues={},weapon='pulse',music=false,schema=3,purchases={},spent={},current_mission=1,discovered={}}
 for _,mission in ipairs(g.data.missions)do
  g.saved.earned['mission:'..mission.id]=true
  g.saved.earned['skill:'..mission.id]=true
 end
 g.dialog='menu';g.paused=true;g.intro_needed=false
 self.polish_last_view=nil;self.polish_view_frames=0
 print('DEFOLD POLISH MENU READY score='..g:total())
end
function F.choose(self)
 if not self.polish_ui_test then return end
 local g=self.g;local target=g.m.secret.position;local start,pickup
 -- Use a real reachable approach and a real ground hit target, preserving all
 -- enemies/cover. The collection point stays inside the normal pickup radius.
 for i=0,15 do
  local angle=i*math.pi/8;local dx,dz=math.cos(angle),math.sin(angle)
  local candidate={target[1]+dx*2.8,target[2]+dz*2.8}
  local approach={target[1]+dx*.65,target[2]+dz*.65}
  if not g:blocked(candidate)and not g:blocked(approach)and clear(g,candidate,approach)and clear(g,approach,target)then
   g.p=candidate;View.follow(g,0,true)
   local x,y=View.project(g,approach,0)
   if x>170 and x<1110 and y>120 and y<600 and free_floor_target(g,x,y)then
    g:navigate(approach)
    if #g.path>0 then start,pickup=candidate,approach;break end
   end
  end
 end
 assert(start and pickup,'No genuine clickable treasure approach: '..g.m.id)
 g.p={start[1],start[2]};g.path={};g.bullets={};g.over=false;g.solved=false;g.paused=false;g.dialog=nil;g.peaceful=false;g.invulnerable=999
 for _,enemy in ipairs(g.enemies)do enemy.timer=999;enemy.warning=0;enemy.patrol=nil end
 g.zoom_focus=nil;View.follow(g,0,true)
 self.polish_pickup=pickup;self.polish_before=g:total();self.polish_found=false;self.polish_hint_seen=false;self.polish_last_view=nil;self.polish_view_frames=0
 print('DEFOLD POLISH CHOOSE mission='..g.m.id..' distance='..string.format('%.3f',distance(g.p,target))..' score='..g:total())
end
function F.update(self,dt)
 if not self.polish_ui_test then return end
 local g=self.g
 if g.dialog then return end
 if #g.path==0 then self.visual_clock=0 end
 if not self.polish_pickup then return end
 local px,py=View.project(g,self.polish_pickup,0)
 local hx,hy=View.project(g,g.p,0);local _,head=View.project(g,{g.p[1],g.p[2]-2.1*.8},2.1*.6)
 local state=g:treasure_state()
 local view=table.concat({g.m.id,string.format('%.3f',g.zoom or 1),math.floor(px),math.floor(py),math.floor(hx),math.floor(hy)},':')
 if view==self.polish_last_view then self.polish_view_frames=self.polish_view_frames+1 else self.polish_last_view=view;self.polish_view_frames=0 end
 if self.polish_view_frames==2 then
  print('DEFOLD POLISH VIEW mission='..g.m.id..' zoom='..string.format('%.3f',g.zoom or 1)..' x='..math.floor(px)..' y='..math.floor(py)..' hero_height='..string.format('%.3f',head-hy)..' score='..g:total()..' discovered='..tostring(state.discovered)..' scale='..string.format('%.3f',state.scale or 0))
 end
 if g.navigation_focus=='treasure'and not self.polish_hint_seen then
  self.polish_hint_seen=true
  print('DEFOLD POLISH HINT TRACKS mission='..g.m.id..' goal='..g:mission_state().goal_kind..' credits='..g:credits())
 end
 if not self.polish_found and g.saved.earned['secret:'..g.m.id]then
  self.polish_found=true
  local delta=g:total()-self.polish_before
  assert(delta==g.data.rewards['secret:'..g.m.id],'Treasure award must be genuine and unique')
  print('DEFOLD POLISH TREASURE FOUND mission='..g.m.id..' score='..g:total()..' delta='..delta..' shots='..g.shots_fired)
 end
end
return F
