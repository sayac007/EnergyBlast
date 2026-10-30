-- Current-round objectives and optional treasure are deliberately separate.
-- This module owns navigation state, never native game objects or shot previews.
local F={}
local Shots=require 'main.projectiles'
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function valid_index(g,index)
 return type(index)=='number'and index==index and index%1==0 and index>=1 and index<=#g.data.missions
end
local function nearest(g,predicate)
 local best,d=nil,math.huge
 for _,enemy in ipairs(g.enemies or{})do
  if not enemy.optional and enemy.hp>0 and predicate(enemy)then
   local n=distance(g.p,enemy.p);if n<d then best,d=enemy,n end
  end
 end
 return best
end
local function open_bonus(g)
 local best,point,d=nil,nil,math.huge
 for _,task in ipairs(g.bonus and g.bonus.tasks or{})do if not task.done then
  local p=task.p
  if not p then for _,entity in ipairs(g.enemies)do if entity.optional and entity.task==task and entity.hp>0 then p=entity.p;break end end end
  if p then local n=distance(g.p,p);if n<d then best,point,d=task,p,n end end
 end end
 return best,point
end
function F.bind(g)
 -- Discovery persists independently of a temporary spoken hint and is harmless
 -- to old saves: only known mission IDs with boolean true values are retained.
 if type(g.saved.discovered)~='table'then g.saved.discovered={}end
 local valid={};for _,mission in ipairs(g.data.missions)do valid[mission.id]=true end
 for id,value in pairs(g.saved.discovered)do if not valid[id]or value~=true then g.saved.discovered[id]=nil end end
 function g:discover_treasure()
  if not self.m.secret or not self:treasure_state().available then return false end
  if type(self.saved.discovered)~='table'then self.saved.discovered={}end
  if not self.saved.discovered[self.m.id]then self.saved.discovered[self.m.id]=true;self.changed();return true end
  return false
 end
 function g:treasure_state()
  local cfg=self.data.treasure_guidance or{}
  local secret=self.m.secret
  if not secret then return{available=false,discovered=false,tracking=false,visible=false,distance=0,proximity=0,scale=cfg.far_scale or 1.4,search_radius=cfg.search_radius or 1.8}end
  local d=distance(self.p,secret.position);local rewarded=self.saved.earned['secret:'..self.m.id]==true
  local available=self.data.optional_replay and not self.treasure_collected or(not self.data.optional_replay and not rewarded)
  local discovered=(self.data.optional_replay and rewarded)or(type(self.saved.discovered)=='table'and self.saved.discovered[self.m.id]==true)or self:level()>0 or self.solved or d<(cfg.discover_radius or 4)
  local delta={secret.position[1]-self.p[1],secret.position[2]-self.p[2]};local dir=d>.000001 and{delta[1]/d,delta[2]/d}or{1,0}
  local occluded=d>.05 and Shots.ray(self.p,dir,d-.05,self:active())~=nil
  local proximity=math.max(0,math.min(1,1-d/(cfg.discover_radius or 4)))
  return{available=available,reward_earned=rewarded,replay=available and rewarded,position=secret.position,hint=secret.hint_landmark or secret.position,discovered=discovered==true,
   distance=d,proximity=proximity,tracking=available and(self.navigation_focus=='treasure'or self.solved==true),
   visible=available and discovered==true,occluded=occluded,scale=(cfg.far_scale or 1.4)+((cfg.near_scale or 2.3)-(cfg.far_scale or 1.4))*proximity,
   search_radius=cfg.search_radius or 1.8}
 end
 function g:update_treasure()
  local cfg=self.data.treasure_guidance;if not cfg then return end
  local state=self:treasure_state()
  if state.available and state.discovered then self:discover_treasure()end
  self.secret_visible=state.visible
  if state.available and state.distance<cfg.pickup_radius and not state.occluded and not self:blocked(state.position)then
   self.treasure_collected=true;local amount=self:award('secret:'..self.m.id);self.secret_visible=false
   self.status=amount>0 and('SCHATZ GEFUNDEN + '..amount..' STERNE')or'SCHATZ ERNEUT GEFUNDEN - STERNE SCHON GESPEICHERT'
   if self.solved or amount==0 then
    if not self:track_bonus()then self.navigation_focus='objective';self.say('flow_no_treasure')end
   else self.say('combat_loot')end
  end
 end
 function g:start_index()
  if valid_index(self,self.saved.current_mission)then return self.saved.current_mission end
  for index,mission in ipairs(self.data.missions)do
   if not self.saved.earned['mission:'..mission.id]then return index end
  end
  return #self.data.missions>0 and #self.data.missions or 1
 end
 function g:remember_mission(index)
  if not valid_index(self,index)then return false end
  if self.saved.current_mission~=index then self.saved.current_mission=index;self.changed()end
  return true
 end
 function g:next_index()
  if self.index and self.index<#self.data.missions then return self.index+1 end
 end
 function g:next_mission()
  if not self.solved then return false end
  local index=self:next_index()
  if not index then self.dialog='menu';self.paused=true;self.say(self.data.campaign_enabled and'defold_campaign_clear'or'flow_final');return false end
  self:remember_mission(index)
  if self.choose then self.choose(index)else self:load(index)end
  return true
 end
 function g:resume_mission()
  if self.cancel_controls then self.cancel_controls()end
  if self.over and not self.solved then
   if self.choose then self.choose(self.index)else self:load(self.index)end
   return true
  end
  self.paused=false;self.dialog=nil;self.held=false
  if self.solved then
   self.over=false;self.pending_win=nil;self.peaceful=true;self.bullets={}
   for _,enemy in ipairs(self.enemies)do enemy.warning=0 end
   self.status=self.data.campaign_enabled and'MISSION GESCHAFFT - WEITER ZUR NAECHSTEN MISSION'or'MISSION GESCHAFFT - SCHATZ OPTIONAL'
  end
  return true
 end
 function g:track_treasure()
  if not self.m.secret or not self:treasure_state().available then return false end
  self.navigation_focus='treasure';self.status='FOLGE DEM SCHATZZEICHEN';self.say('flow_treasure');return true
 end
 function g:track_bonus()
  local task=open_bonus(self);if not task then return false end
  self.navigation_focus='bonus';self.status='BONUS FREIWILLIG - FOLGE DEM ZEICHEN'
  self:guide();return true
 end
 function g:track_objective()
  self.navigation_focus='objective';return true
 end
 function g:search_loot()
  if not self.solved then return false end
  self:resume_mission()
  if self:treasure_state().available then self.navigation_focus='treasure';self.say('flow_loot')
  elseif not self:track_bonus()then self:guide()end
  return true
 end
 function g:guide()
  local state=self:mission_state()
  if self.data.campaign_enabled then
   if state.primary_done then self.say('defold_campaign_clear')
   elseif state.goal_kind=='sequence'then self.say('defold_campaign_sequence')
   elseif state.goal_kind=='exit'then self.say('flow_exit')
   else self.say(self.m.voice or'defold_campaign_mission')end
   return state
  end
  -- Info must explain a remaining bonus, even if the chest's one-time reward
  -- was earned in a previous app session. Explicit chest tracking stays valid.
  if self.data.optional_replay and self.navigation_focus~='treasure'and(state.primary_done or state.treasure_rewarded)then
   local task=open_bonus(self)
   if task then self.navigation_focus='bonus';state=self:mission_state()end
  end
  if state.goal_kind=='treasure'then self.say('flow_treasure')
  elseif state.goal_kind=='exit'then self.say('flow_exit')
  elseif state.goal_kind=='bonus'then local kind=state.goal_bonus_kind;self.say(kind=='wait'and'bonus_wait'or(kind=='sequence'or kind=='pattern')and'bonus_sequence'or'bonus_prism')
  elseif state.primary_done then self.say(state.treasures_remaining==0 and'flow_no_treasure'or'flow_loot')
  else self.say(self.m.voice or(self.m.id=='dock'and'raid_dock'or'combat_'..self.m.id))end
  return state
 end
 function g:mission_state()
  local state={enemies=0,relays=0,sequence_remaining=0,treasures_remaining=0,
   primary_done=self.solved==true,exit_required=self.m.exit_required==true,
   exit_open=self:open(),bonus_done=0,bonus_total=0,bonus_rewarded=0,bonus_replay=0,treasure_rewarded=false,treasure_replay=false,headline='',goal=nil,goal_kind=nil}
  for _,enemy in ipairs(self.enemies)do if not enemy.optional and enemy.hp>0 then
   if enemy.kind=='relay'then state.relays=state.relays+1
   elseif enemy.kind~='sequence'then state.enemies=state.enemies+1 end
  end end
  if self.m.sequence then state.sequence_remaining=math.max(0,#self.m.sequence-self.sequence_progress)end
  if self.m.secret then
   local treasure=self:treasure_state();state.treasures_remaining=treasure.available and 1 or 0
   state.treasure_rewarded=treasure.reward_earned==true;state.treasure_replay=treasure.replay==true
  end
  local bonuses=self.bonus and self.bonus.tasks or{}
  for _,bonus in ipairs(bonuses)do
   state.bonus_total=state.bonus_total+1;if bonus.done then state.bonus_done=state.bonus_done+1 end
   if self.saved.earned[bonus.key]then state.bonus_rewarded=state.bonus_rewarded+1 end
   if bonus.replay then state.bonus_replay=state.bonus_replay+1 end
  end
  if self.solved then
   state.headline=self.data.campaign_enabled and'MISSION GESCHAFFT - NAECHSTE MISSION'or state.treasures_remaining>0 and'MISSION GESCHAFFT - SCHATZ OPTIONAL'or state.bonus_done<state.bonus_total and'MISSION GESCHAFFT - BONI OPTIONAL'or'ALLES GEFUNDEN - NAECHSTE MISSION'
  elseif self.m.kind=='escort'and self.drone and not self.drone.arrived then
   state.headline='BEGLEITE DIE DROHNE';state.goal=self.drone.p;state.goal_kind='drone'
  elseif state.sequence_remaining>0 then
   state.headline='LICHTERFOLGE '..self.sequence_progress..'/'..#self.m.sequence
   local p={0,0};local nodes=self.m.sequence_nodes or{}
   for _,node in ipairs(nodes)do p[1]=p[1]+node[1];p[2]=p[2]+node[2]end
   if #nodes>0 then p={p[1]/#nodes,p[2]/#nodes+1.1}else p=self.m.goal end
   state.goal=p;state.goal_kind='sequence' -- Observation area, never the correct next answer.
  elseif state.relays>0 then
   state.headline='RELAIS AUSSCHALTEN: '..state.relays
   local target=nearest(self,function(e)return e.kind=='relay'end);state.goal=target and target.p;state.goal_kind='relay'
  elseif state.enemies>0 and not(self.m.kind=='escort'and self.drone and self.drone.arrived)then
   local target=nearest(self,function(e)return e.kind~='relay'and e.kind~='sequence'end)
   state.headline=target and target.trap_shield and((target.trapped or 0)>0 and'SCHILD AUS - JETZT TREFFEN'or'FALLE LEGEN - WAECHTER LOCKEN')or('GEGNER: '..state.enemies)
   state.goal=target and target.p;state.goal_kind=target and target.trap_shield and'trap'or'enemy'
  elseif self.m.exit_required then
   state.headline=self:open()and'FOLGE DEM PFEIL ZUM AUSGANG'or'TOR LAEDT - ZUM AUSGANG'
   state.goal=self.m.goal;state.goal_kind='exit'
  else state.headline='MISSION ABSCHLIESSEN'end
  if state.treasures_remaining>0 and(self.solved or self.navigation_focus=='treasure')then
   local secret=self.m.secret
   local revealed
   if self.data.treasure_guidance then revealed=self:treasure_state().discovered else revealed=self.solved or self:level()>0 or distance(self.p,secret.position)<4 end
   state.goal=revealed and secret.position or secret.hint_landmark;state.goal_kind='treasure'
  end
  if self.navigation_focus=='bonus'or(self.solved and(state.treasures_remaining==0 or(state.treasure_replay and self.navigation_focus~='treasure')))then
   local task,p=open_bonus(self)
   if task then state.goal=p;state.goal_kind='bonus';state.goal_bonus_kind=task.kind;state.headline='BONUS FREIWILLIG: '..(task.title or'ZUSATZSTERNE')end
  end
  return state
 end
end
return F
