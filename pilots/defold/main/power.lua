-- Permanent bonus power is derived solely from known, once-earned bonus keys.
-- It never spends stars, trusts a saved level or changes collision/movement size.
local P={}
function P.bind(g)
 function g:power_state()
  local cfg=self.data.bonus_power
  local state={enabled=cfg~=nil,count=0,total=0,tier=0,title='ENTDECKER',min_health=self.data.player.hit_points,visual_scale=1,damage_multiplier=1,shield_max=0,cloak_multiplier=1,detection_multiplier=1,regen_fraction=0,milestones={}}
  if not cfg then return state end
  for _,mission in ipairs(self.data.missions)do
   for _,id in ipairs({'prism','pattern'})do
    if mission.bonuses and mission.bonuses[id]and self.data.rewards['bonus:'..id..':'..mission.id]then
     state.total=state.total+1
     if self.saved.earned['bonus:'..id..':'..mission.id]==true then state.count=state.count+1 end
    end
   end
  end
  for index,step in ipairs(cfg.steps)do
   if state.count>=step.bonuses then
    state.step=index;state.title=step.title;state.min_health=step.health;state.visual_scale=step.visual_scale;state.damage_multiplier=step.damage_multiplier;state.shield_max=step.shield;state.cloak_multiplier=step.detection_multiplier;state.detection_multiplier=step.detection_multiplier;state.regen_fraction=cfg.health_regen_fraction
   elseif not state.next then
    state.next={count=step.bonuses,title=step.title,min_health=step.health,damage_multiplier=step.damage_multiplier,shield_max=step.shield,visual_scale=step.visual_scale,detection_multiplier=step.detection_multiplier}
    state.next_count=step.bonuses;state.next_health=step.health
   end
  end
  for _,threshold in ipairs(cfg.milestones)do
   for _,step in ipairs(cfg.steps)do if step.bonuses==threshold then
    state.milestones[#state.milestones+1]={count=threshold,title=step.title,min_health=step.health}
    if state.count>=threshold then state.tier=state.tier+1 end
    break
   end end
  end
  return state
 end
 function g:reset_power()
  local state=self:power_state()
  self.max_shield=state.shield_max;self.shield=self.max_shield
  self.shield_since_hit=0;self.shield_regen_charge=0
  self.power_flash=0;self.power_gain=nil
 end
 function g:refresh_power(previous)
  local state=self:power_state()
  if not state.enabled then return false end
  local old_max=self.max_hp or self:max_health()
  local old_shield=self.max_shield or 0
  self.max_hp=self:max_health()
  -- Reward growth immediately without erasing existing damage or reviving defeat.
  if self.hp and self.hp>0 then self.hp=math.min(self.max_hp,self.hp+math.max(0,self.max_hp-old_max))end
  self.max_shield=state.shield_max
  self.shield=math.min(self.max_shield,math.max(0,self.shield or 0)+math.max(0,self.max_shield-old_shield))
  if previous and state.count>previous.count then
   self.power_flash=2;self.power_gain={count=state.count,title=state.title,health=self.max_hp,damage_multiplier=state.damage_multiplier,shield_max=state.shield_max,visual_scale=state.visual_scale}
   self.fx[#self.fx+1]={kind='power',p={self.p[1],self.p[2]},age=0,life=1.5}
   self.cooldown=math.min(self.cooldown or 0,self:weapon_stats().cooldown)
   return true
  end
  return false
 end
 function g:power_hit()
  if not self.data.bonus_power or(self.shield or 0)<=0 then return false end
  self.shield=self.shield-1;self.shield_since_hit=0;self.shield_regen_charge=0
  self.regen_since_hit=0;self.regen_charge=0;self.regenerating=false
  self.invulnerable=self.data.combat.hit_invulnerability;self.feedback=.2
  self.fx[#self.fx+1]={kind='shield',p={self.p[1],self.p[2]},age=0,life=.25}
  if self.sfx then self.sfx('bounce')end
  return true
 end
 function g:recover_shield(dt)
  local cfg=self.data.bonus_power
  if not cfg or self.hp<=0 or(self.max_shield or 0)<=0 then return end
  self.shield_since_hit=(self.shield_since_hit or 0)+dt
  if self.shield>=self.max_shield then self.shield_regen_charge=0;return end
  if self.shield_since_hit<cfg.shield_regen_delay then return end
  self.shield_regen_charge=(self.shield_regen_charge or 0)+dt*math.max(1,self.max_shield*cfg.shield_regen_fraction)
  local points=math.floor(self.shield_regen_charge+.000001)
  if points>0 then self.shield=math.min(self.max_shield,self.shield+points);self.shield_regen_charge=self.shield_regen_charge-points end
 end
 function g:detection_multiplier()
  local gear=self:owns('cloak2')and .5 or self:owns('cloak')and .825 or 1
  return gear*self:power_state().detection_multiplier
 end
end
return P
