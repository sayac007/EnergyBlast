-- Explicit native power regression fixture. It seeds an old bonus ledger and
-- stages the player; live GUI input, projectiles and the production bonus rule
-- must earn the new step. No task completion, hit or reward is forced here.
local View=require 'main.view'
local Regions=require 'main.hit_regions'
local Shots=require 'main.projectiles'
local Layout=require 'main.layout'
local Stage=require 'main.stage_view'
local F={}
local profiles={first=0,thousand=7,million=11}
-- Bounds of the actual active illustrated_hero.gltf quad, independently of the
-- deliberately padded touch rectangle. Apply its real native world transform.
local quad={{-.725,0,0},{.725,0,0},{-.725,1.26,-1.68},{.725,1.26,-1.68}}
local function bounds(self,stage)
 local g=self.g;local matrix=go.get_world_transform(self.hero)
 local view,projection
 if stage then local w,h=window.get_size();view,projection=Stage.matrices(w,h,g.p,self.hero_visual_scale or 1)end
 local x1,y1,x2,y2=math.huge,math.huge,-math.huge,-math.huge
 for _,vertex in ipairs(quad)do
  local point=matrix*vmath.vector4(vertex[1],vertex[2],vertex[3],1)
  local x,y
  if stage then
   local clip=projection*view*point
   x=Stage.left+(clip.x/clip.w+1)*Stage.width/2;y=Stage.bottom+(clip.y/clip.w+1)*Stage.height/2
  else x,y=g.project(g,{point.x,point.z},point.y)end
  x1=math.min(x1,x);y1=math.min(y1,y);x2=math.max(x2,x);y2=math.max(y2,y)
 end
 local left,bottom,right,top=Layout.left,Layout.bottom,Layout.right,Layout.top
 if stage then left,bottom,right,top=Stage.left,Stage.bottom,Stage.left+Stage.width,Stage.bottom+Stage.height end
 assert(x1>=left-8 and x2<=right+8 and y1>=bottom-8 and y2<=top+8,
  string.format('Actual native hero clips %s: %.2f %.2f %.2f %.2f',stage and'stage'or'world',x1,y1,x2,y2))
 return x1,y1,x2,y2
end
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function segment_distance(p,a,b)
 local dx,dz=b[1]-a[1],b[2]-a[2]
 local t=math.max(0,math.min(1,((p[1]-a[1])*dx+(p[2]-a[2])*dz)/math.max(.00001,dx*dx+dz*dz)))
 return distance(p,{a[1]+dx*t,a[2]+dz*t})
end
local function clear_shot(g,a,target)
 local d=distance(a,target.p)
 if d<.001 or Shots.ray(a,{(target.p[1]-a[1])/d,(target.p[2]-a[2])/d},d-.03,g:active())then return false end
 for _,zone in ipairs(g.m.absorbers or{})do if segment_distance(zone.position,a,target.p)<zone.radius+.05 then return false end end
 if g.m.sanctuary and segment_distance(g.m.sanctuary.position,a,target.p)<g.m.sanctuary.radius+.05 then return false end
 for _,enemy in ipairs(g.enemies)do if enemy~=target and enemy.hp>0 and segment_distance(enemy.p,a,target.p)<.65 then return false end end
 return true
end
local function stage(self)
 local g=self.g;local task=g.bonus.tasks[2];local target=task.targets[1];local found
 assert(task.kind=='wait','Power GUI test uses the genuine green timing challenge')
 for _,radius in ipairs({3.6,4.4,2.8,5.2})do
  for i=0,31 do
   local angle=math.pi/2+i*math.pi/16
   local p={target.p[1]+math.cos(angle)*radius,target.p[2]+math.sin(angle)*radius}
   if not g:blocked(p)and not g:is_safe(p)and clear_shot(g,p,target)then
    g.p=p;View.follow(g,0,true);local r=Regions.bounds(g,target)
    if r.x>190 and r.x<1090 and r.y>145 and r.y<565 and Regions.visible(g,target)and not Regions.own(g,r.x,r.y)then found=p;break end
   end
  end
  if found then break end
 end
 assert(found,'No actual clickable power challenge approach')
 g.path={};g.bullets={};g.over=false;g.solved=false;g.paused=false;g.dialog=nil;g.peaceful=false;g.invulnerable=999
 for _,enemy in ipairs(g.enemies)do enemy.timer=999;enemy.warning=0;enemy.patrol=nil end
 self.power_task=task;self.power_phase='before';self.power_frames=0;self.power_ready=nil;self.power_after=0
 self.power_before=g:power_state();self.power_score=g:total();self.power_wallet=g:wallet();self.power_hp_before=g.max_hp
end
function F.init(self)
 local profile=sys.get_config_string('project.power_ui_test','')
 if not profiles[profile]then return end
 self.power_ui_test=profile;self.g.power_ui_test=true;self.muted=true
 local g=self.g;self.power_restarted=g.saved.power_fixture_profile==profile
 if not self.power_restarted then
  g.saved={earned={},clues={},weapon='prism',character='hero',music=false,schema=3,purchases={prism=true},spent={prism=100},current_mission=2,discovered={},power_fixture_profile=profile}
  if profile~='first'then g.saved.purchases.armor=true;g.saved.spent.armor=160 end
  for _,mission in ipairs(g.data.missions)do
   for _,prefix in ipairs({'mission:','skill:','secret:'})do g.saved.earned[prefix..mission.id]=true end
  end
  local remaining=profiles[profile]
  for _,mission in ipairs(g.data.missions)do for _,id in ipairs({'prism','pattern'})do
   local key='bonus:'..id..':'..mission.id
   if key~='bonus:pattern:citadel'and remaining>0 then g.saved.earned[key]=true;remaining=remaining-1 end
  end end
  assert(remaining==0,'Only existing distinct bonus keys can seed prior progression')
  g.changed()
 end
 g.dialog='menu';g.paused=true;g.intro_needed=false
 local state=g:power_state();local expected=profiles[profile]+(self.power_restarted and 1 or 0)
 assert(state.count==expected,'Native process must retain earned bonus progression')
 assert(g:owns('prism')and(profile=='first'or g:owns('armor')),'Previously purchased equipment remains owned')
 print('DEFOLD POWER MENU READY profile='..profile..' restarted='..tostring(self.power_restarted)..' count='..state.count..' score='..g:total()..' wallet='..g:wallet())
end
function F.choose(self)
 if not self.power_ui_test then return end
 local g=self.g;assert(g.m.id=='citadel','Power test must select real timing mission')
 stage(self)
 local count=g:power_state().count
 print('DEFOLD POWER CHOOSE profile='..self.power_ui_test..' restarted='..tostring(self.power_restarted)..' count='..count..' hp='..g.max_hp..' shield='..g.max_shield)
end
local function rendered(self,prefix)
 local g=self.g;local state=g:power_state();local scale=go.get_scale(self.hero)
 local fx=go.get(msg.url(nil,self.hero,'model'),'power_fx')
 local shield=self.hero_power_shield and go.get_scale(self.hero_power_shield).x or 0
 assert(scale.x>0 and fx.x>0 and fx.x<=1,'Real native power material and scale remain finite')
 local x1,y1,x2,y2=bounds(self,false)
 print(prefix..' profile='..self.power_ui_test..' count='..state.count..' hp='..g.max_hp..' shield='..g.max_shield..' scale='..string.format('%.5f',scale.x)..' opacity='..string.format('%.5f',fx.x)..' strength='..string.format('%.5f',fx.y)..' shield_scale='..string.format('%.5f',shield)..' shots='..g.shots_fired..' score='..g:total()..' wallet='..g:wallet())
 print(string.format('DEFOLD POWER WORLD BOUNDS PASS count=%d zoom=%.2f left=%.2f bottom=%.2f right=%.2f top=%.2f',state.count,g.zoom or 1,x1,y1,x2,y2))
end
function F.update(self,dt)
 if not self.power_ui_test then return end
 if self.g.dialog=='power'then
  self.power_panel_seen=true;self.power_stage_frames=(self.power_stage_frames or 0)+1
  if self.power_stage_frames==8 then
   local x1,y1,x2,y2=bounds(self,true)
   print(string.format('DEFOLD POWER STAGE BOUNDS PASS count=%d left=%.2f bottom=%.2f right=%.2f top=%.2f',self.g:power_state().count,x1,y1,x2,y2))
  end
  return
 end
 if self.g.dialog or not self.power_phase then return end
 local g=self.g;local task=self.power_task
 if self.power_panel_seen and self.power_phase=='done'and not self.power_resumed_logged then
  assert(not g.paused,'Closing the power panel resumes the same playable round')
  self.power_resumed_logged=true;print('DEFOLD POWER PANEL CLOSED PASS count='..g:power_state().count)
 end
 self.visual_clock=0;self.power_frames=self.power_frames+1
 if self.power_phase=='before'then
  if self.power_frames==90 then
   rendered(self,'DEFOLD POWER RENDER BEFORE');self.power_native_before=go.get_scale(self.hero).x
   if self.power_restarted then
    assert(task.replay and task.rewarded,'Earned bonus must be available for replay without further power')
    self.power_score=g:total();self.power_wallet=g:wallet()
   end
  end
  if self.power_frames>=90 and task.green and not self.power_ready then
   self.power_ready=true;local r=Regions.bounds(g,task.targets[1])
   print('DEFOLD POWER SHOT READY profile='..self.power_ui_test..' x='..math.floor(r.x)..' y='..math.floor(r.y)..' count='..g:power_state().count)
  end
  if task.done then
   assert(g.shots_fired>0,'Only a live GUI shot can complete the power challenge')
   local after=g:power_state();local expected=self.power_before.count+(self.power_restarted and 0 or 1)
   assert(after.count==expected,'Exactly one distinct bonus advances power; replay does not')
   assert(g.max_hp==g:max_health()and g.hp==g.max_hp,'Earned growth immediately increases actual health')
   assert(g.shield==g.max_shield and g.max_shield==after.shield_max,'Earned growth immediately strengthens the real shield')
   local award=self.power_restarted and 0 or g.data.rewards[task.key]
   assert(g:total()==self.power_score+award and g:wallet()==self.power_wallet+award,'Bonus stars and wallet follow the one-time production award')
   assert(g:owns('prism')and(self.power_ui_test=='first'or g:owns('armor')),'Power gain cannot erase purchases')
   if not self.power_restarted then assert(g.max_hp>self.power_hp_before and after.damage_multiplier>self.power_before.damage_multiplier,'A new bonus immediately increases health and firepower')end
   self.power_phase='after';g.changed()
   print('DEFOLD POWER EARNED profile='..self.power_ui_test..' count='..after.count..' hp='..g.max_hp..' shield='..g.max_shield..' delta='..award)
  end
 elseif self.power_phase=='after'then
  self.power_after=self.power_after+dt
  if self.power_after>2.4 then
   local scale=go.get_scale(self.hero).x
   if not self.power_restarted then assert(scale>self.power_native_before*1.02,'The actual native hero visibly grows after the bonus')end
   rendered(self,'DEFOLD POWER RENDER AFTER')
   self.power_restore={g.p[1],g.p[2]};self.power_phase='north';self.power_north_age=0
   g.zoom_control:set(1.75)
   -- Use a real free northern floor close to the reflector/arena boundary.
   local north
   for row=1,20 do for column=0,10 do
    local p={column-5,g.data.arena[2]+.5+row*.1}
    if not g:blocked(p)then north=p;break end
   end;if north then break end end
   assert(north,'Power zoom regression needs an actual walkable north boundary')
   g.p=north;View.follow(g,0,true)
  end
 elseif self.power_phase=='north'then
  self.power_north_age=self.power_north_age+dt
  if self.power_north_age>1 and not self.power_north_logged then
   self.power_north_logged=true;rendered(self,'DEFOLD POWER MAX ZOOM NORTH BOUNDS PASS')
  end
  if self.power_north_age>1.5 then
   g.zoom_control:set(1);g.p=self.power_restore;View.follow(g,0,true)
   self.power_phase='restore';self.power_restore_age=0
  end
 elseif self.power_phase=='restore'then
  self.power_restore_age=self.power_restore_age+dt
  if self.power_restore_age>.35 then
   bounds(self,false);self.power_phase='done';g.changed()
   print('DEFOLD POWER GAIN AND NATIVE GROWTH PASS profile='..self.power_ui_test..' replay='..tostring(self.power_restarted))
  end
 end
end
return F
