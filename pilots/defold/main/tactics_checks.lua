-- Optional relay reflection and readable sequence timing in the actual combat path.
-- Isolated physical shots supplement checks against every configured relay map.
local Combat=require 'main.combat'
local Shots=require 'main.projectiles'
local Objectives=require 'main.objectives'
local Timing=require 'main.sequence_timing'
local M={}
local function copy(value)
 if type(value)~='table'then return value end
 local out={};for key,item in pairs(value)do out[key]=copy(item)end;return out
end
local function close(a,b)return math.abs(a-b)<.000001 end
function M.run(active,archived)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 local function fresh(index,data)
  local g=Combat.new(copy(data or active));g:load(index or 3)
  g.invulnerable=999;g.spoken={};g.say=function(id)g.spoken[#g.spoken+1]=id end
  for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.scan_clock=999;e.patrol=nil end
  return g
 end
 local function approach(g,target)
  local origin={g.p[1],g.p[2]};g.clock=5
  for _,radius in ipairs({1.2,1.8,2.6,3.4})do for angle=0,31 do
   local a=angle*math.pi/16;local p={target.p[1]+math.cos(a)*radius,target.p[2]+math.sin(a)*radius}
   local direction=Combat.norm({target.p[1]-p[1],target.p[2]-p[2]})
   if not g:blocked(p)and not g:is_safe(p)and not Shots.ray(p,direction,radius-.03,g:active())then
    g.p=origin;g:navigate(p)
    if #g.path>0 and Combat.dist(g.path[#g.path],p)<.5 then return p end
   end
  end end
 end
 local direct_count=0
 for index,mission in ipairs(active.missions)do
  for ordinal in ipairs(mission.relays or{})do
   local g=fresh(index);local relays={};local boss
   for _,e in ipairs(g.enemies)do if e.kind=='relay'then relays[#relays+1]=e elseif e.boss then boss=e end end
   local relay=relays[ordinal];check(relay and not relay.shield,'active switch has no mandatory reflection shield '..mission.id..':'..ordinal)
   if boss then
    local hp=boss.hp;g:hit(boss,1,100)
    check(boss.hp==hp and g:locked(boss),'boss still requires live relays, independent of reflection '..mission.id)
    check(g.spoken[#g.spoken]=='defold_relays_free','active relay instruction offers direct shots '..mission.id)
   end
   local point=approach(g,relay);check(point~=nil,'reachable direct firing spot exists for relay '..mission.id..':'..ordinal)
   g.p=point;g.path={};g.aim=Combat.norm({relay.p[1]-point[1],relay.p[2]-point[2]});g.cooldown=0
   local bounces;local ordinary_hit=g.hit
   g.hit=function(self,target,count,damage)if target==relay then bounces=count end;return ordinary_hit(self,target,count,damage)end
   local hp=relay.hp;g:fire()
   check(g.shots_fired==1 and relay.hp==hp,'direct relay attack begins as a timed projectile '..mission.id..':'..ordinal)
   for frame=1,160 do Shots.update(g,.025);if relay.hp<=0 then break end end
   check(relay.hp==0 and bounces==0,'real unreflected projectile disables relay '..mission.id..':'..ordinal)
   direct_count=direct_count+1
  end
 end
 check(direct_count>=10,'regression exercises switches across all advanced relay missions')
 -- A physical bank shot is still a valid freely chosen alternative.
 local g=fresh(3);local relay
 for _,e in ipairs(g.enemies)do if e.kind=='relay'then relay=e;break end end
 local guard={p={8,5},hp=9,max_hp=9,timer=999,warning=0,direction={1,0},burst=1}
 relay.p={2,0};g.enemies={relay,guard};g.walls={{r={-6,-2.2,12,.2},type='cover'}}
 g.m.sanctuary={position={-8,5},radius=1.2};g.m.absorbers={};g.m.gate_rect=nil;g.p={-2,0};g.path={};g.bullets={};g.aim=Combat.norm({4,-4})
 local hit_bounces;local ordinary_hit=g.hit
 g.hit=function(self,target,count,damage)if target==relay then hit_bounces=count end;return ordinary_hit(self,target,count,damage)end
 g:fire();for frame=1,160 do Shots.update(g,.025);if relay.hp<=0 then break end end
 local actual_bounce=false;for _,fx in ipairs(g.fx)do actual_bounce=actual_bounce or fx.kind=='bounce'end
 check(relay.hp==0 and hit_bounces==1 and actual_bounce,'ordinary cover reflection physically hits the switch as an optional alternative')
 check(guard.hp==9,'free relay targeting does not damage unrelated hostiles')
 -- Defensive compatibility: older runtime relay metadata cannot reintroduce a lock.
 g=fresh(3);relay=nil
 for _,e in ipairs(g.enemies)do if e.kind=='relay'then relay=e;break end end
 relay.shield=true;g:hit(relay,0)
 check(relay.hp==0,'a stale relay shield flag cannot restore forced bank shots in current rules')
 -- The change is limited to switches, not combat shields and trap mechanics.
 g=fresh(1);local shielded=g.enemies[1];local hp=shielded.hp
 g:hit(shielded,0)
 check(shielded.hp==hp,'actual dangerous shielded enemies retain their combat rule')
 g:hit(shielded,1)
 check(shielded.hp<hp,'a real combat shield is still defeated by a reflected attack')
 g=fresh(3);local boss
 for _,e in ipairs(g.enemies)do if e.boss then boss=e end end
 check(g:locked(boss),'boss is initially protected by switches')
 for _,e in ipairs(g.enemies)do if e.kind=='relay'then g:hit(e,0)end end
 check(not g:locked(boss),'directly solving every switch releases the boss')
 hp=boss.hp;g:hit(boss,1,100)
 check(boss.hp<hp,'released boss can be damaged after switches')
 -- Every actual sequence mission shares the same deliberately slower clock.
 for index,mission in ipairs(active.missions)do if mission.sequence then
  g=fresh(index)
  local function state(clock)g.sequence_clock=clock;return Timing.state(g)end
  local s=state(0)
  check(close(s.step_seconds,1.8)and close(s.lit_seconds,1.2)and close(s.pause_seconds,2.4),'twofold readable sequence timing '..mission.id)
  check(close(s.cycle_seconds,7.8)and s.lit and s.order==mission.sequence[1],'full three-signal cycle includes a clear replay pause '..mission.id)
  for slot,order in ipairs(mission.sequence)do
   local start=(slot-1)*1.8
   check(state(start).lit and state(start).order==order,'signal starts at its scheduled boundary '..mission.id..':'..slot)
   check(state(start+1.05).lit and Timing.is_lit(g,order),'signal remains readable beyond the former short flash '..mission.id..':'..slot)
   check(not state(start+1.2).lit and not Timing.is_lit(g,order),'separation gap begins at its precise boundary '..mission.id..':'..slot)
   check(not state(start+1.7).lit,'signal does not flicker during its dark separation '..mission.id..':'..slot)
  end
  check(not state(5.4).lit and not state(7.79).lit,'longer whole-pattern pause is visibly dark '..mission.id)
  check(state(7.8).lit and state(7.8).order==mission.sequence[1],'pattern repeats without an extra or skipped signal '..mission.id)
  local first
  for _,e in ipairs(g.enemies)do if e.kind=='sequence'and e.order==mission.sequence[1]then first=e;break end end
  g.sequence_clock=6;g:hit(first,0)
  check(g.sequence_progress==1,'children may answer the remembered order during the pause '..mission.id)
  g.paused=true;local clock=g.sequence_clock;g:update(.05)
  check(g.sequence_clock==clock,'opening a menu does not skip the readable pattern '..mission.id)
 end end
 -- Explicit frozen data retains the original challenge and timings.
 check(archived and not archived.campaign_enabled,'historical regression rules are supplied separately')
 local old=fresh(3,archived);local old_relay
 for _,e in ipairs(old.enemies)do if e.kind=='relay'then old_relay=e;break end end
 hp=old_relay.hp;old:hit(old_relay,0)
 check(old_relay.shield and old_relay.hp==hp and old.spoken[#old.spoken]=='raid_relays','archived switches keep their exact original shield/cue behavior')
 old:hit(old_relay,1);check(old_relay.hp==0,'archived bank-shot success remains unchanged')
 old=fresh(5,archived);old.sequence_clock=.65;local before=Timing.state(old)
 check(close(before.step_seconds,.9)and close(before.lit_seconds,.6)and close(before.cycle_seconds,4.6)and not before.lit,'frozen sequence timing remains the old short signal')
 old.sequence_clock=.95;check(Timing.state(old).lit and Timing.state(old).order==old.m.sequence[2],'frozen second signal remains in its original time slot')
 return n
end
return M
