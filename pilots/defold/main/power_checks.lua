-- Real bonus, combat, regeneration and save-reconstruction checks for power gains.
local Combat=require 'main.combat'
local Bonus=require 'main.bonus'
local Shots=require 'main.projectiles'
local M={}
local function keys(data)
 local result={}
 for _,mission in ipairs(data.missions)do for _,id in ipairs({'prism','pattern'})do result[#result+1]='bonus:'..id..':'..mission.id end end
 return result
end
local function store(data,count)
 local s={earned={},clues={'reactor:1'},schema=3,purchases={},spent={},weapon='pulse',music=false,character='dragon'}
 for i,key in ipairs(keys(data))do if i<=count then s.earned[key]=true end end
 return s
end
function M.run(data)
 if not data.bonus_power then return 0 end
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(saved,index)
  local g=Combat.new(data,saved);g:load(index or 1)
  for _,enemy in ipairs(g.enemies)do enemy.timer=999;enemy.warning=0;enemy.patrol=nil end
  return g
 end
 local function tick(g,seconds)
  for i=1,math.ceil(seconds/.025)do g:update(.025)end
 end
 local list=keys(data)
 local expected={20,30,35,40,80,160,400,1000,10000,100000,400000,1000000}
 local previous={health=15,damage=1,shield=0,scale=1,cloak=1}
 for count=0,#list do
  local g=fresh(store(data,count));local power=g:power_state();local weapon=g:weapon_stats()
  check(power.enabled and power.count==count and power.total==12,'only actual known distinct bonus keys set power '..count)
  check(power.min_health==(expected[count]or data.player.hit_points)and g.hp==g.max_hp and g.max_hp==power.min_health,'each bonus applies its exact energy immediately on load '..count)
  check(g.shield==power.shield_max and g.max_shield==power.shield_max,'old saved bonuses restore full protective shield '..count)
  check(weapon.cooldown>=.12 and weapon.cooldown<=data.combat.fire_cooldown,'fire cadence is bounded even at absurd power '..count)
  check(power.visual_scale>=1 and power.visual_scale<=1.75,'visual growth remains bounded '..count)
  check(power.detection_multiplier>=.1 and power.detection_multiplier<=1,'camouflage is real and bounded '..count)
  check(g.power_flash==0 and g.power_gain==nil,'loading old bonuses does not replay a fresh reward animation '..count)
  if count>0 then
   check(g.max_hp>previous.health and weapon.damage>previous.damage and g.max_shield>previous.shield,'every single new bonus improves health damage and shield '..count)
   check(power.visual_scale>previous.scale and power.detection_multiplier<previous.cloak,'every single bonus grows actor and improves camouflage '..count)
  end
  if count<12 then check(power.next and power.next.count==count+1 and power.next.min_health==expected[count+1],'next reward preview matches next distinct bonus '..count)
  else check(not power.next and not power.next_count and power.tier==5,'million-energy final milestone has no fictional future reward')end
  check(#power.milestones==5 and power.milestones[1].min_health==20 and power.milestones[2].min_health==30 and power.milestones[3].min_health==40 and power.milestones[4].min_health==1000 and power.milestones[5].min_health==1000000,'milestone display derives exact requested progression '..count)
  previous={health=g.max_hp,damage=weapon.damage,shield=g.max_shield,scale=power.visual_scale,cloak=power.detection_multiplier}
 end
 -- Each newly earned key applies in the current round, without reload or purchases.
 for count=0,11 do
  local current=fresh(store(data,count));current.hp=current.max_hp-1
  local old_max,old_shield,old_hp=current.max_hp,current.shield,current.hp
  local total=current:total();local credits=current:credits()
  local amount=current:award(list[count+1]);local state=current:power_state()
  check(amount==data.rewards[list[count+1]]and state.count==count+1,'real award advances exactly one known level '..count)
  check(current.max_hp==expected[count+1]and current.hp==old_hp+current.max_hp-old_max,'every live gain preserves prior damage while growing energy '..count)
  check(current.shield>old_shield and current.shield==current.max_shield,'each live reward grants the added shield capacity immediately '..count)
  check(current.power_gain.count==count+1 and current.power_gain.health==current.max_hp and current.power_flash==2,'each live gain emits an actual presentation event '..count)
  check(current:total()==total+amount and current:credits()==credits,'power grants no extra clue or duplicated currency '..count)
  local resulting_hp,resulting_shield=current.hp,current.shield;current:award(list[count+1])
  check(current:power_state().count==count+1 and current.hp==resulting_hp and current.shield==resulting_shield,'duplicate award cannot heal or grow hero '..count)
 end
 local bad=store(data,0);bad.earned['bonus:prism:unknown']=true;bad.earned['bonus:prism:reactor']='true';bad.earned['mission:reactor']=true;bad.power_level=999999999
 local g=fresh(bad)
 check(g:power_state().count==0 and g.max_hp==15,'unknown keys strings mission rewards and forged level cannot grant power')
 -- Complete an actual swept bank shot, with the real first arena and shield rules.
 g=fresh(store(data,0));local crystal=g.bonus.tasks[1].targets[1];g.enemies={crystal};g.p={-9,crystal.p[2]};g.hp=g.max_hp-1;g.aim={-1,0};local before=g:total()
 g:fire();for frame=1,160 do Shots.update(g,.025)end
 check(g.bonus.tasks[1].done and g:total()==before+100,'real reflected bonus hit awards original stars')
 check(g:power_state().count==1 and g.max_hp==20 and g.hp==19,'same real hit adds five energy while preserving existing one damage')
 check(g.shield==3 and g.max_shield==3 and g.power_flash>0 and g.power_gain.health==20,'new bonus grants real shield and native power-up event immediately')
 check(g:weapon_stats().damage==2 and g:weapon_stats().cooldown<.24,'next actual shots already use increased damage and cadence')
 local gain=g.power_gain;local shield=g.shield;g:hit(crystal,1);g:award(list[1])
 check(g:power_state().count==1 and g.shield==shield and g.power_gain==gain and g:total()==before+100,'repeated target hits cannot farm stats shield or stars')
 g:load(1);crystal=g.bonus.tasks[1].targets[1];g:hit(crystal,1)
 check(g:power_state().count==1 and g.max_hp==20 and g:total()==100,'replaying same earned bonus never advances permanent power')
 -- Sequence and timing completion go through their real task logic as well.
 g=fresh(store(data,1));local task=g.bonus.tasks[2]
 g:hit(task.targets[task.sequence[2]],0);check(g:power_state().count==1,'wrong light sequence cannot grant a power step')
 for _,order in ipairs(task.sequence)do g:hit(task.targets[order],0)end
 check(task.done and g:power_state().count==2 and g.max_hp==30 and g:total()==250,'real completed sequence grants next power step and stars')
 local s=store(data,3);s.earned['bonus:pattern:citadel']=nil;g=fresh(s,2);task=g.bonus.tasks[2]
 g:hit(task.targets[1],0);check(not task.done and g:power_state().count==3,'red timing shot cannot brute-force a power reward')
 Bonus.update(g,3.01);g:hit(task.targets[1],0)
 check(task.done and g:power_state().count==4 and g.max_hp==40,'green timing completion earns fourth distinct step')
 -- Shield protects health, records no health damage and recharges after delay.
 g=fresh(store(data,1));g.p={-9,1};g:hit_player()
 check(g.hp==20 and g.shield==2 and g.damage==0,'shield truly absorbs a hit instead of only drawing a ring')
 g.invulnerable=0;g:hit_player();g.invulnerable=0;g:hit_player();g.invulnerable=0;g:hit_player()
 check(g.shield==0 and g.hp==19 and g.damage==1,'depleted shield allows real subsequent health damage')
 local hp=g.hp;tick(g,2.5);check(g.shield==0 and g.hp==hp,'shield does not refill before its delay')
 tick(g,1.7);check(g.shield>=1 and g.shield<=g.max_shield,'shield recharges during real active simulation')
 tick(g,4);check(g.shield==g.max_shield,'shield recharge clamps at its actual maximum')
 for _,mode in ipairs({'paused','background','tactical_pause'})do
  g=fresh(store(data,12));g.p={-9,1};g.shield=0;g.hp=g.max_hp-100;g.shield_since_hit=10;g.regen_since_hit=10;g[mode]=true
  tick(g,1);check(g.shield==0 and g.hp==g.max_hp-100,'no regeneration leaks through '..mode)
 end
 -- Million-scale health recovers in a useful duration and remains numerically safe.
 g=fresh(store(data,12));g.p={-9,1};g.hp=500000;g.regen_since_hit=4;tick(g,1)
 check(g.hp>=525000 and g.hp<=526000,'large health uses meaningful proportional recovery rather than multi-day healing')
 g.hp=g.max_hp-1;g.regen_since_hit=4;tick(g,.1)
 check(g.hp==g.max_hp and g.shield<=g.max_shield,'large-number recovery never overflows maximum')
 -- Real detection distance is reduced; damage/glow never bypass objective rules.
 g=fresh(store(data,0));g.enemies={{p={-9,1},hp=2,max_hp=2,timer=0,warning=0,direction={1,0},burst=1}};g.p={-5,1};g:update(.025)
 check(g.enemies[1].warning>0,'unpowered nearby player is detected')
 g=fresh(store(data,12));g.enemies={{p={-9,1},hp=2,max_hp=2,timer=0,warning=0,direction={1,0},burst=1}};g.p={-5,1};g:update(.025)
 check(g.enemies[1].warning==0,'actual enemy acquisition respects stronger invisibility')
 local max=g.max_hp;local target=g.enemies[1];target.shield=true;g:hit(target,0,g:weapon_stats().damage)
 check(target.hp==2,'absurd firepower cannot ignore a required reflected shot')
 target.shield=false;target.boss=true;g.enemies[#g.enemies+1]={p={7,2},kind='relay',hp=1,max_hp=1,timer=999,warning=0}
 g:hit(target,1,g:weapon_stats().damage);check(target.hp==2,'power cannot bypass live boss-relay prerequisites')
 target.boss=false;g:hit(target,1,g:weapon_stats().damage)
 check(target.hp==0,'actual powered shot damage can defeat a non-locked enemy')
 local purchased=store(data,12);purchased.purchases={armor=true,armor2=true,armor3=true,armor4=true,prism=true,nova2=true,cloak2=true};purchased.spent={armor=160,armor2=300,armor3=450,armor4=650,prism=100,nova2=650};purchased.weapon='nova2'
 g=fresh(purchased)
 check(g.max_hp==1000020 and g:owns('armor4'),'purchased armor remains additive to million-energy bonus')
 check(g:weapon_stats().damage==4000 and g:weapon_stats().cooldown==.12,'equipped higher-tier weapon remains stronger and bounded')
 check(math.abs(g:detection_multiplier()-.05)<.000001,'purchased cloak stacks with permanent bonus camouflage')
 local total,wallet=g:total(),g:wallet();local restored=fresh(g.saved)
 check(restored.max_hp==1000020 and restored.shield==100000 and restored:weapon_stats().damage==4000,'saved earned keys reconstruct all real power and equipment')
 check(restored:total()==total and restored:wallet()==wallet and restored.saved.character=='dragon'and restored.saved.music==false and #restored.saved.clues==1,'power migration preserves score spending hero music and hints')
 g=fresh(store(data,0));g.hp=0;g.over=true;g:award(list[1])
 check(g.hp==0 and g.over and g.max_hp==20,'a reward cannot resurrect an already lost round')
 return n
end
return M
