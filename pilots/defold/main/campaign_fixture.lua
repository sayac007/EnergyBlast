-- Explicit active-campaign GUI fixture: old ledger, quiet hostile AI and real
-- reachable player staging. It never forces hits, mission completion or awards.
local View=require 'main.view'
local Regions=require 'main.hit_regions'
local Layout=require 'main.layout'
local Swarm=require 'main.swarm'
local Shots=require 'main.projectiles'
local F={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function clear(g,a,b)
 local d=distance(a,b)
 return d<.001 or not Shots.ray(a,{(b[1]-a[1])/d,(b[2]-a[2])/d},d-.03,g:active())
end
local function seed(g)
 g.saved={earned={},clues={'reactor:1'},weapon='prism',character='hero',music=false,schema=3,
  purchases={prism=true,armor=true,armor2=true,armor3=true,armor4=true},
  spent={prism=100,armor=160,armor2=300,armor3=450,armor4=650},current_mission=1,
  discovered={reactor=true},campaign_fixture_seeded=true}
 -- These twelve actual 0.13 bonus keys previously implied million-health power.
 for i=1,6 do local mission=g.data.missions[i]
  for _,prefix in ipairs({'mission:','skill:','secret:','bonus:prism:','bonus:pattern:'})do g.saved.earned[prefix..mission.id]=true end
 end
 g.changed()
end
local function check_ledger(self)
 local g=self.g
 assert(g:total()==self.campaign_score and g:wallet()==self.campaign_wallet,'Campaign migration must retain old points and debits')
 assert(g:owns('prism')and g:owns('armor4')and g.saved.weapon=='prism','Campaign must preserve old purchased equipment')
 assert(g.hp>0 and g.hp<=100 and g.max_hp<=100,'Active campaign health is capped including old armor')
end
local function quiet(g)
 g.invulnerable=999
 for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil;e.scan_clock=999;e.replication_clock=999;e.speed=0 end
end
local function stage_drone(self,stay_at_spawn)
 local g=self.g;local target
 for _,e in ipairs(g.enemies)do if e.hp>0 and not e.optional and e.kind~='sequence'and not g:locked(e)then target=e;break end end
 assert(target,'Drone GUI fixture needs a genuine unlocked hostile')
 local found=stay_at_spawn and{g.p[1],g.p[2]}or nil
 if not stay_at_spawn then for _,radius in ipairs({4.4,3.6,5.2,2.8})do
  for i=0,31 do
   local angle=i*math.pi/16
   local p={target.p[1]+math.cos(angle)*radius,target.p[2]+math.sin(angle)*radius}
   if not g:blocked(p)and not g:is_safe(p)and clear(g,p,target.p)then
    g.p=p;View.follow(g,0,true);local r=Regions.bounds(g,target)
    local w,h=window.get_size();local v=View.viewport(g,w,h)
    if r.x>v.left+80 and r.x<v.right-80 and r.y>v.bottom+80 and r.y<v.top-90 and Regions.visible(g,target)and not Regions.own(g,r.x,r.y)then found=p;break end
   end
  end
  if found then break end
 end end
 assert(found,'No real visible drone target approach in '..g.m.id)
 if stay_at_spawn then assert(g:is_safe(),'The first real drone attack must launch from the actual protected spawn')end
 g.path={};g.bullets={};self.campaign_target=target;self.campaign_launch_origin={g.p[1],g.p[2]}
 self.campaign_stock=g.attack_drone.stock;self.campaign_launched=false;self.campaign_killed=false;self.campaign_lightning=false;self.campaign_cancelled=false
 self.campaign_prior_zoom=g.zoom;self.campaign_prior_saved_zoom=g.saved.zoom;self.campaign_view_restored=false
 self.campaign_user_zoom=nil
end
local function start_stress(self)
 local g=self.g
 -- Accelerate existing family timers, preserving the real finite split rule.
 -- Birth locations, generation limits, native allocations and cap remain real.
 for _,e in ipairs(g.enemies)do if e.can_replicate then e.replication_clock=.01 end end
 self.campaign_stress_age=0
end
function F.init(self)
 local mode=sys.get_config_string('project.campaign_ui_test','')
 if mode==''or mode=='0'then return end
 assert(self.g.data.campaign_enabled and #self.g.data.missions==16,'Campaign GUI must use current sixteen-mission rules, not archived fixtures')
 self.campaign_ui_mode=mode;self.g.campaign_ui_test=true;self.muted=true
 local g=self.g;local restarted=g.saved.campaign_fixture_seeded==true
 if not restarted then seed(g)end
 self.campaign_score=g:total();self.campaign_wallet=g:wallet()
 assert(self.campaign_score==4350 and self.campaign_wallet==2690,'Old million-power ledger has its original score and purchases')
 g.dialog='menu';g.paused=true;g.intro_needed=false
 print('DEFOLD CAMPAIGN FIXTURE READY mode='..mode..' restarted='..tostring(restarted)..' score='..g:total()..' wallet='..g:wallet())
end
function F.choose(self)
 if not self.campaign_ui_mode then return end
 local g=self.g;check_ledger(self)
 assert(g:is_safe()and distance(g.p,g.m.spawn)<.001 and distance(g.p,g.m.sanctuary.position)<.001,'Every actual mission opens at its protected Zikkurat')
 assert(not g.m.bonuses and not g.m.secret and g.bonus.total==0 and #g.bonus.tasks==0,'Current campaign has no hidden optional rewards')
 assert(not self.chest and not self.chest_glow,'Removed campaign treasure cannot allocate native chest models')
 for _,e in ipairs(g.enemies)do assert(not e.optional,'Campaign must not leave hidden bonus enemies')end
 local state=g:mission_state();assert(state.bonus_total==0 and state.treasures_remaining==0,'HUD counters cannot retain old hidden rewards')
 quiet(g);g.over=false;g.paused=false;g.dialog=nil;g.path={};g.bullets={}
 self.campaign_frames=0;self.campaign_ready=false;self.campaign_matte_age=nil;self.campaign_matte_done=false;self.campaign_minimum_seen=false
 self.campaign_target=nil;self.campaign_last_drone_ui=nil;self.campaign_selection_age=0;self.campaign_target_logged=false
 if self.campaign_ui_mode:match('^drone_')then stage_drone(self,false)
 elseif self.campaign_ui_mode=='next'and g.index==1 then stage_drone(self,true)
 elseif self.campaign_ui_mode=='next'and g.index==2 then
  assert(math.abs(g.zoom-self.campaign_prior_zoom)<.00001 and g.saved.zoom==self.campaign_prior_saved_zoom,'Changing missions restores the temporary targeting overview without saving it')
  print('DEFOLD CAMPAIGN DRONE NEXT VIEW RESTORED PASS zoom='..g.zoom)
 elseif self.campaign_ui_mode=='stress'then start_stress(self)end
 print('DEFOLD CAMPAIGN CHOOSE mission='..g.index..' id='..g.m.id..' protected=true hp='..g.max_hp..' arena='..g.arena[3]..'x'..g.arena[4]..' bonus=0 treasure=0 score='..g:total()..' wallet='..g:wallet())
end
local function model_ready(self)
 local g=self.g;local actual=0
 assert(self.arena and go.exists(self.arena)and self.ground and go.exists(self.ground),'Selected campaign has actual native world models')
 assert(self.sanctuary and go.exists(self.sanctuary),'Protected start has an actual native sanctuary')
 for _,e in ipairs(g.enemies)do if e.hp>0 then
  assert(e.node and go.exists(e.node),'Every visible hostile has a real native model')
  actual=actual+1
 end end
 return actual
end
local function watch_drone(self,dt)
 local g=self.g;local d=g.attack_drone;local target=self.campaign_target
 if not target then return end
 assert(g.shots_fired==0 and #g.path==0,'Drone gestures must never fire the hero or move them')
 if self.campaign_ui_mode=='drone_zoom'and g.saved.zoom~=self.campaign_prior_saved_zoom and not self.campaign_user_zoom then
  assert(d.phase=='flying'and g.saved.zoom==g.zoom,'The test must deliberately change and save zoom during the actual drone flight')
  assert(math.abs(g.zoom-math.min(View.max_zoom,View.minimum_zoom(g)+.15))<.00001,'A deliberate plus step advances from the actual overview without jumping to the old camera')
  self.campaign_user_zoom=g.zoom;print('DEFOLD CAMPAIGN DRONE USER ZOOM DURING FLIGHT PASS zoom='..g.zoom)
 end
 assert(g.saved.zoom==(self.campaign_user_zoom or self.campaign_prior_saved_zoom),'A temporary drone overview cannot overwrite the saved user zoom')
 if g.drone_ui then
  self.campaign_last_drone_ui=g.drone_ui.mode
  assert(d.stock==self.campaign_stock,'Selecting or cancelling a drone cannot spend stock')
  if g.drone_ui.mode=='target'then
   assert(g.drone_control.overview and math.abs(g.zoom-View.minimum_zoom(g))<.00001,'Target selection exposes the real complete map without saving zoom')
  end
  self.campaign_selection_age=self.campaign_selection_age+dt
  if self.campaign_selection_age>.25 then
   self.campaign_selection_age=0
   print('DEFOLD CAMPAIGN DRONE SELECTION SAFE mode='..g.drone_ui.mode..' stock='..d.stock..' shots=0 path=0')
  end
 elseif self.campaign_last_drone_ui and d.phase=='ready'and not self.campaign_launched then
  self.campaign_cancelled=true;self.campaign_last_drone_ui=nil
  assert(d.stock==self.campaign_stock,'Explicit cancel keeps every drone')
  assert(math.abs(g.zoom-self.campaign_prior_zoom)<.00001 and not g.drone_control.overview,'Cancel immediately restores the prior camera zoom')
  print('DEFOLD CAMPAIGN DRONE CANCEL PASS stock='..d.stock..' shots=0 path=0 zoom='..g.zoom)
 end
 if self.campaign_frames>=8 then
  local r=Regions.bounds(g,target);local token=math.floor(r.x)..':'..math.floor(r.y)..':'..string.format('%.5f',g.zoom)
  if token~=self.campaign_target_logged then self.campaign_target_logged=token
  print('DEFOLD CAMPAIGN DRONE TARGET '..math.floor(r.x)..' '..math.floor(r.y)..' hp='..target.hp)
  end
 end
 if d.phase=='flying'then
  self.campaign_last_drone_ui=nil
  if not self.campaign_user_zoom then assert(g.drone_control.overview and math.abs(g.zoom-View.minimum_zoom(g))<.00001,'An in-flight badge tap must not end the temporary targeting view')end
  assert(d.stock==self.campaign_stock-1 and d.launched==1,'Exactly one genuine launch spends exactly one drone')
  if not self.campaign_launched and d.age>.025 and distance(d.p,self.campaign_launch_origin)>.05 then
   assert(self.attack_drone_node and go.exists(self.attack_drone_node),'Live drone flight has a native model')
   self.campaign_launched=true
   print('DEFOLD CAMPAIGN DRONE FLYING PASS stock='..d.stock..' age='..string.format('%.3f',d.age)..' target_hp='..target.hp..' hero_shots=0')
   local x,y=g.project(g,g.p,.4);local w,h=window.get_size();local v=View.viewport(g,w,h)
   print('DEFOLD CAMPAIGN INFLIGHT BADGE '..math.floor(math.max(v.left+51,math.min(v.right-51,x-100)))..' '..math.floor(math.max(v.bottom+55,math.min(v.top-55,y+20))))
  end
 end
 for _,fx in ipairs(g.fx)do if fx.kind=='lightning'and self.fragments[fx]then
  local objects=self.fragments[fx]
  for _,node in ipairs(objects)do if go.exists(node)then self.campaign_lightning=true end end
 end end
 if target.hp<=0 and d.kills==1 and self.campaign_lightning and not self.campaign_killed then
  assert(self.campaign_launched and d.stock==self.campaign_stock-1,'Animated impact follows a timed physical flight')
  self.campaign_killed=true
  self.campaign_impact_clock=g.clock
  print('DEFOLD CAMPAIGN DRONE IMPACT / NATIVE LIGHTNING PASS stock='..d.stock..' kills='..d.kills..' hero_shots=0')
 end
 if self.campaign_killed and not g.drone_control.overview and not self.campaign_view_restored then
  local expected=self.campaign_user_zoom or self.campaign_prior_zoom
  assert(math.abs(g.zoom-expected)<.00001,'After impact the original or deliberately selected user zoom wins')
  if not self.campaign_user_zoom then assert(g.clock-self.campaign_impact_clock>.7,'The overview remains until the native electric impact animation has played')end
  self.campaign_view_restored=true
  print((self.campaign_user_zoom and'DEFOLD CAMPAIGN DRONE USER VIEW KEPT PASS zoom='or'DEFOLD CAMPAIGN DRONE FLIGHT VIEW RESTORED PASS zoom=')..g.zoom)
 end
end
local function minimum_view(self,dt)
 local g=self.g;local minimum=View.minimum_zoom(g)
 if g.zoom>minimum+.00001 then return end
 if not self.campaign_minimum_seen then
  local a=g.arena;local w,h=window.get_size();local v=View.viewport(g,w,h)
  local x1,y1=View.project(g,{a[1],a[2]},0);local x2,y2=View.project(g,{a[1]+a[3],a[2]+a[4]},0)
  assert(math.abs(x1-v.left)<.08 and math.abs(x2-v.right)<.08 and math.abs(y1-v.top)<.08 and math.abs(y2-v.bottom)<.08,
   string.format('Minimum view must fit arena: corners %.3f %.3f %.3f %.3f viewport %.3f %.3f %.3f %.3f window %dx%d',x1,y1,x2,y2,v.left,v.top,v.right,v.bottom,w,h))
  local mx,my
  if v.left>Layout.left+2 then mx=(Layout.left+v.left)/2;my=(v.bottom+v.top)/2
  else assert(v.bottom>Layout.bottom+2,'Fixture needs a real nonplayable letterbox');mx=(v.left+v.right)/2;my=(Layout.bottom+v.bottom)/2 end
  assert(not View.field(g,mx,my),'Letterbox is not playable floor')
  self.campaign_minimum_seen=true;self.campaign_matte_age=0
  print('DEFOLD CAMPAIGN MINIMUM VIEW mission='..g.index..' zoom='..string.format('%.5f',g.zoom)..' matte_x='..math.floor(mx)..' matte_y='..math.floor(my))
 end
 if self.campaign_matte_age then
  self.campaign_matte_age=self.campaign_matte_age+dt
  assert(g.shots_fired==0 and #g.path==0,'Letterbox input cannot fire or create a walk path')
  if self.campaign_matte_age>1 and not self.campaign_matte_done then
   self.campaign_matte_done=true;print('DEFOLD CAMPAIGN MATTE INPUT IGNORED PASS mission='..g.index)
  end
 end
end
function F.update(self,dt)
 if not self.campaign_ui_mode then return end
 local g=self.g
 if self.campaign_ui_mode=='next'and g.dialog=='win'and not self.campaign_win_logged then
  assert(g.solved and self.campaign_killed,'A real drone impact must finish the actual first mission')
  self.campaign_win_logged=true;print('DEFOLD CAMPAIGN REAL WIN READY next='..tostring(g:next_index()))
 end
 if g.dialog then return end
 self.campaign_frames=(self.campaign_frames or 0)+1
 check_ledger(self)
 if self.campaign_frames==8 then
  local actual=model_ready(self);self.campaign_ready=true
  print('DEFOLD CAMPAIGN SCENE READY mission='..g.index..' models='..actual..' hp='..g.max_hp..' shots='..g.shots_fired)
 end
 watch_drone(self,dt)
 if self.campaign_ui_mode=='1'or self.campaign_ui_mode=='migration'then minimum_view(self,dt)end
 if self.campaign_ui_mode=='stress'then
  self.campaign_stress_age=self.campaign_stress_age+dt
  for _,e in ipairs(g.enemies)do if e.can_replicate and not e.replication_used then e.replication_clock=math.min(e.replication_clock,.01)end end
  local alive=Swarm.alive(g)
  assert(alive<=50,'Native stress population cannot exceed the production cap')
  if alive==50 and self.campaign_stress_age>1 and not self.campaign_stress_logged then
   local actual=model_ready(self);assert(actual==50 and g.swarm_spawned>0,'Fifty hostiles must come from real bounded offspring and native allocation')
   self.campaign_stress_logged=true
   print('DEFOLD CAMPAIGN FIFTY NATIVE HOSTILES PASS alive=50 models='..actual..' born='..g.swarm_spawned)
  end
 end
end
return F
