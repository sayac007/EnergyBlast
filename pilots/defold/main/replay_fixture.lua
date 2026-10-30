-- Explicit old-save GUI fixture. Never changes or completes a reward task.
-- Only player staging and hostile AI are controlled; shots, walls, hit testing,
-- bonus sequencing, pickup and the persistent reward ledger remain production.
local View=require 'main.view'
local Regions=require 'main.hit_regions'
local Shots=require 'main.projectiles'
local Objectives=require 'main.objectives'
local F={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function clear(g,a,b)
 local d=distance(a,b);if d<.001 then return true end
 return not Shots.ray(a,{(b[1]-a[1])/d,(b[2]-a[2])/d},d-.03,g:active())
end
local function segment_distance(p,a,b)
 local dx,dz=b[1]-a[1],b[2]-a[2]
 local t=math.max(0,math.min(1,((p[1]-a[1])*dx+(p[2]-a[2])*dz)/math.max(.00001,dx*dx+dz*dz)))
 return distance(p,{a[1]+dx*t,a[2]+dz*t})
end
local function clear_shot(g,a,target)
 if not clear(g,a,target.p)then return false end
 for _,zone in ipairs(g.m.absorbers or{})do if segment_distance(zone.position,a,target.p)<zone.radius+.05 then return false end end
 if g.m.sanctuary and segment_distance(g.m.sanctuary.position,a,target.p)<g.m.sanctuary.radius+.05 then return false end
 for _,enemy in ipairs(g.enemies)do if enemy~=target and enemy.hp>0 and segment_distance(enemy.p,a,target.p)<.65 then return false end end
 return true
end
local function point_visible(g,e)
 local r=Regions.bounds(g,e)
 return r.x>180 and r.x<1100 and r.y>140 and r.y<580 and Regions.visible(g,e)and not Regions.own(g,r.x,r.y)
end
local function stage_pattern(self)
 local g=self.g;local task=g.bonus.tasks[2];local found
 for _,radius in ipairs({2.8,3.6,4.4,2.1})do
  for i=0,31 do
   local angle=math.pi/2+i*math.pi/16
   local p={task.p[1]+math.cos(angle)*radius,task.p[2]+math.sin(angle)*radius}
   if not g:blocked(p)and not g:is_safe(p)and distance(p,g.m.secret.position)>1.6 then
    g.p=p;View.follow(g,0,true);local valid=true
    for _,target in ipairs(task.targets)do if not clear_shot(g,p,target)or not point_visible(g,target)then valid=false;break end end
    if valid then found=p;break end
   end
  end
  if found then break end
 end
 assert(found,'No genuine native shooting approach for '..g.m.id)
 self.replay_task=task;self.replay_phase='pattern';self.replay_stable=0;self.replay_ready_token=nil;self.replay_guided=false
end
local function free_floor_target(g,x,y)
 if Regions.own(g,x,y)or Regions.enemy(g,x,y)then return false end
 if Objectives.can_trap(g)then
  local px,py=View.project(g,g.p,.4)
  local bx=math.max(198,math.min(1082,px+87));local by=math.max(154,math.min(566,py+20))
  if math.abs(x-bx)<=46 and math.abs(y-by)<=46 then return false end
 end
 return true
end
local function stage_chest(self)
 local g=self.g;local target=g.m.secret.position;local found
 assert(g:treasure_state().available,'Pattern staging must not accidentally collect replay chest')
 for i=0,31 do
  local angle=i*math.pi/16;local dx,dz=math.cos(angle),math.sin(angle)
  local start={target[1]+dx*2.8,target[2]+dz*2.8};local approach={target[1]+dx*.65,target[2]+dz*.65}
  if not g:blocked(start)and not g:blocked(approach)and clear(g,start,approach)and clear(g,approach,target)then
   g.p=start;View.follow(g,0,true);local x,y=View.project(g,approach,0)
   if x>180 and x<1100 and y>130 and y<590 and free_floor_target(g,x,y)then
    g:navigate(approach)
    if #g.path>0 then found=approach;break end
   end
  end
 end
 assert(found,'No real replay chest walking approach for '..g.m.id)
 g.path={};g.bullets={};g.held=false;g.aiming=false;g.touch:cancel();g.navigation_focus='treasure'
 self.replay_pickup=found;self.replay_phase='chest';self.replay_stable=0
end
function F.init(self)
 if sys.get_config_string('project.replay_ui_test','0')~='1'then return end
 self.replay_ui_test=true;self.muted=true
 local g=self.g;local restarted=g.saved.replay_fixture_seeded==true
 if not restarted then
  g.saved={earned={},clues={},weapon='prism',music=false,schema=3,purchases={armor=true,prism=true},spent={armor=160,prism=100},current_mission=1,discovered={},replay_fixture_seeded=true}
  for _,mission in ipairs(g.data.missions)do for _,prefix in ipairs({'mission:','skill:','secret:','bonus:prism:','bonus:pattern:'})do g.saved.earned[prefix..mission.id]=true end end
  g.changed()
 end
 self.replay_score=g:total();self.replay_wallet=g:wallet()
 assert(self.replay_score==4350 and self.replay_wallet==4090,'Fixture must keep its complete old reward/purchase ledger')
 assert(g:owns('armor')and g:owns('prism'),'Old equipment remains owned')
 local prior_say=g.say
 g.say=function(id)
  self.replay_last_voice=id
  if self.replay_phase then print('DEFOLD REPLAY VOICE mission='..g.m.id..' id='..id)end
  prior_say(id)
 end
 g.dialog='menu';g.paused=true;g.intro_needed=false
 print('DEFOLD REPLAY MENU READY score='..g:total()..' wallet='..g:wallet()..' restarted='..tostring(restarted))
end
function F.choose(self)
 if not self.replay_ui_test then return end
 local g=self.g
 assert(g:total()==self.replay_score and g:wallet()==self.replay_wallet,'Reload must preserve both scores')
 g.path={};g.bullets={};g.over=false;g.solved=true;g.paused=false;g.dialog=nil;g.peaceful=true;g.invulnerable=999
 for _,enemy in ipairs(g.enemies)do enemy.timer=999;enemy.warning=0;enemy.patrol=nil end
 local alive=0
 for _,task in ipairs(g.bonus.tasks)do
  assert(not task.done and task.replay and task.rewarded,'Earned bonus must rearm for this visit')
  for _,target in ipairs(task.targets)do assert(target.hp>0 and target.node and go.exists(target.node),'Replay target has a real native model');alive=alive+1 end
 end
 local treasure=g:treasure_state()
 assert(treasure.available and treasure.replay and treasure.reward_earned,'Old rewarded chest is replayable')
 self.replay_visits=self.replay_visits or{};self.replay_visits[g.m.id]=(self.replay_visits[g.m.id]or 0)+1
 self.replay_last_voice=nil;self.replay_hint_seen=false;self.replay_task_logged=nil;self.replay_complete_delay=nil
 stage_pattern(self)
 print('DEFOLD REPLAY CHOOSE mission='..g.m.id..' visit='..self.replay_visits[g.m.id]..' alive='..alive..' bonus_done='..g.bonus.completed..' treasure='..tostring(treasure.available)..' score='..g:total()..' wallet='..g:wallet())
end
function F.update(self,dt)
 if not self.replay_ui_test or self.g.dialog or not self.replay_phase then return end
 local g=self.g
 assert(g:total()==self.replay_score and g:wallet()==self.replay_wallet,'Replay must never duplicate earned stars or spend equipment credit')
 assert(g:owns('armor')and g:owns('prism'),'Replay must preserve equipment')
 self.replay_stable=self.replay_stable+1
 if self.replay_phase=='pattern'then
  local task=self.replay_task
  if not self.replay_guided and g.navigation_focus=='bonus'and self.replay_last_voice and self.replay_last_voice:match('^bonus_')then
   self.replay_guided=true
   print('DEFOLD REPLAY HINT PASS mission='..g.m.id..' goal='..g:mission_state().goal_kind..' voice='..self.replay_last_voice)
  end
  if self.replay_stable==5 then print('DEFOLD REPLAY SCENE READY mission='..g.m.id)end
  local ready=not task.done and(task.kind~='wait'or task.green)
  if ready and self.replay_stable>=5 then
   local target=task.targets[task.kind=='sequence'and task.sequence[task.progress+1]or 1]
   local token=tostring(task.progress)..':'..(task.kind=='wait'and tostring(math.floor(task.clock/5))or'once')
   if token~=self.replay_ready_token then
    self.replay_ready_token=token;local r=Regions.bounds(g,target)
    print('DEFOLD REPLAY SHOT READY mission='..g.m.id..' progress='..task.progress..' x='..math.floor(r.x)..' y='..math.floor(r.y)..' kind='..task.kind)
   end
  end
  if task.done then
   self.replay_complete_delay=(self.replay_complete_delay or 0)+dt
   if not self.replay_task_logged then
    self.replay_task_logged=true
    assert(g.shots_fired>0,'A replay bonus must be solved by an actual shot')
    print('DEFOLD REPLAY BONUS PASS mission='..g.m.id..' shots='..g.shots_fired..' score='..g:total()..' wallet='..g:wallet()..' delta=0')
   end
   if self.replay_complete_delay>.35 then self.replay_complete_delay=nil;self.replay_task_logged=nil;stage_chest(self)end
  end
 elseif self.replay_phase=='chest'then
  if self.replay_stable==5 then
   local x,y=View.project(g,self.replay_pickup,0)
   local state=g:treasure_state();assert(state.visible,'Replayed chest must actually become visible on approach')
   print('DEFOLD REPLAY CHEST READY mission='..g.m.id..' x='..math.floor(x)..' y='..math.floor(y)..' visible='..tostring(state.visible))
  end
  if not g:treasure_state().available then
   self.replay_phase='done';g.changed()
   print('DEFOLD REPLAY CHEST PASS mission='..g.m.id..' score='..g:total()..' wallet='..g:wallet()..' delta=0')
  end
 end
end
return F
