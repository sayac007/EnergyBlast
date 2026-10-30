-- Explicit native regression fixture. It quiets AI and stages reachable free
-- floor, but relay damage comes only from the driver's real screen press.
local View=require 'main.view'
local Regions=require 'main.hit_regions'
local Shots=require 'main.projectiles'
local Timing=require 'main.sequence_timing'
local F={}
local function distance(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function clear(g,a,b)
 local d=distance(a,b)
 return d<.001 or not Shots.ray(a,{(b[1]-a[1])/d,(b[2]-a[2])/d},d-.03,g:active())
end
local function quiet(g)
 g.invulnerable=999
 for _,e in ipairs(g.enemies)do e.timer=999;e.warning=0;e.patrol=nil;e.scan_clock=999;e.replication_clock=999;e.speed=0 end
end
local function stage_relay(self)
 local g=self.g;local relay;local boss
 for _,e in ipairs(g.enemies)do if e.kind=='relay'and not relay then relay=e elseif e.boss then boss=e end end
 assert(relay and boss and g:locked(boss),'Actual dock has two protecting relay switches')
 assert(not relay.shield,'Current switches must not advertise a forced reflection shield')
 self.tactics_relay=relay;self.tactics_relay_hp=relay.hp;self.tactics_boss=boss;self.tactics_boss_hp=boss.hp
 -- This rejected probe cannot damage or complete an objective. It verifies that
 -- the spoken lock instruction does not reintroduce the obsolete wall command.
 g.say('defold_campaign_sequence')
 assert(self.voice_id=='defold_campaign_sequence'and self.voice_left>0,'A prior full instruction really starts before the contextual replacement')
 g:hit(boss,0)
 assert(self.voice_id=='defold_relays_free'and self.voice_left==self.clips.defold_relays_free.seconds,'The new complete instruction immediately replaces the previous one')
 self.tactics_voice_duration=self.voice_left;self.tactics_voice_checked=false
 assert(boss.hp==self.tactics_boss_hp and self.tactics_spoken[#self.tactics_spoken]=='defold_relays_free','Boss lock keeps switches but uses the current free-choice cue')
 local found
 for _,radius in ipairs({3.6,2.8,4.4,2})do
  for i=0,31 do
   local a=i*math.pi/16;local p={relay.p[1]+math.cos(a)*radius,relay.p[2]+math.sin(a)*radius}
   if not g:blocked(p)and not g:is_safe(p)and clear(g,p,relay.p)then
    g.p=p;View.follow(g,0,true);local r=Regions.bounds(g,relay);local w,h=window.get_size();local v=View.viewport(g,w,h)
    if r.x>v.left+70 and r.x<v.right-70 and r.y>v.bottom+75 and r.y<v.top-60 and Regions.visible(g,relay)and not Regions.own(g,r.x,r.y)then found=p;break end
   end
  end
  if found then break end
 end
 assert(found,'Actual relay needs reachable, visible direct firing ground')
 g.path={};g.bullets={};g.cooldown=0
 self.tactics_hit_bounces=nil;self.tactics_relay_shots=g.shots_fired
 local ordinary_hit=g.hit
 g.hit=function(game,target,bounces,damage)
  if target==relay then self.tactics_hit_bounces=bounces end
  return ordinary_hit(game,target,bounces,damage)
 end
end
function F.init(self)
 if sys.get_config_string('project.tactics_ui_test','0')~='1'then return end
 assert(self.g.data.campaign_enabled,'Tactics GUI must use current campaign rules')
 self.tactics_ui_test=true;self.g.tactics_ui_test=true;self.muted=false;self.tactics_spoken={}
 local g=self.g;local say=g.say
 g.say=function(id)
  self.tactics_spoken[#self.tactics_spoken+1]=id
  assert(id~='raid_relays','Active free-choice fixture must never play the old mandatory wall cue')
  say(id)
 end
 g.saved.weapon='pulse';g.saved.purchases={};g.saved.earned={};g.saved.spent={};g.saved.current_mission=1;g.saved.music=false
 g.dialog='menu';g.paused=true;g.intro_needed=false
 print('DEFOLD TACTICS FIXTURE READY')
end
function F.choose(self)
 if not self.tactics_ui_test then return end
 local g=self.g;quiet(g);self.tactics_frames=0;self.tactics_ready=false;self.tactics_relay_done=false
 g.path={};g.bullets={};g.over=false;g.paused=false;g.dialog=nil
 if g.index==3 then stage_relay(self)
 elseif g.index==5 then
  assert(g.m.sequence and #g.m.sequence==3,'Echo mission retains its actual sequence task')
  g.zoom=View.minimum_zoom(g);View.follow(g,0,true)
  g.sequence_clock=0;self.tactics_checkpoint=1
 else error('Tactics fixture expects actual missions3 and5')end
 print('DEFOLD TACTICS CHOOSE mission='..g.index)
end
function F.update(self,dt)
 if not self.tactics_ui_test or self.g.dialog then return end
 local g=self.g;self.tactics_frames=(self.tactics_frames or 0)+1
 if self.tactics_frames==8 then
  assert(self.arena and go.exists(self.arena),'Tactics test has real native world geometry')
  self.tactics_ready=true
  if g.index==3 then
   local r=Regions.bounds(g,self.tactics_relay)
   print('DEFOLD TACTICS RELAY READY '..math.floor(r.x)..' '..math.floor(r.y)..' hp='..self.tactics_relay.hp..' boss_locked=true')
  else
   print('DEFOLD TACTICS SEQUENCE READY')
  end
 end
 if not self.tactics_ready then return end
 if g.index==3 then
  assert(self.tactics_boss.hp==self.tactics_boss_hp and g:locked(self.tactics_boss),'One ordinary relay shot cannot bypass another protecting switch')
  if not self.tactics_voice_checked and self.voice_left<self.tactics_voice_duration-.4 then
   assert(self.voice_id=='defold_relays_free'and self.voice_left>0,'The free-choice instruction must still be playing')
   local remaining=self.voice_left
   for attempt=1,4 do g:hit(self.tactics_boss,0)end
   assert(self.voice_id=='defold_relays_free'and self.voice_left==remaining,'Repeated rejected attacks cannot restart or truncate the current complete instruction')
   self.tactics_voice_checked=true
   print('DEFOLD TACTICS COMPLETE VOICE / CONTEXT REPLACE / NO RESTART PASS remaining='..string.format('%.3f',remaining))
  end
  if self.tactics_relay.hp<=0 and not self.tactics_relay_done then
   assert(g.shots_fired==self.tactics_relay_shots+1 and self.tactics_hit_bounces==0,'Relay damage must be the actual first unreflected screen shot')
   self.tactics_relay_done=true
   print('DEFOLD TACTICS REAL DIRECT RELAY PASS shots=1 bounces=0 boss_locked=true')
  end
 elseif g.index==5 then
  assert(g.sequence_progress==0 and g.shots_fired==0,'Timing observation does not fabricate answers or shoot a puzzle node')
  local checkpoints={.85,1.35,2.05,4,5.8,7.95};local checkpoint=self.tactics_checkpoint
  if checkpoints[checkpoint]and g.sequence_clock>=checkpoints[checkpoint]then
   local state=Timing.state(g)
   print('DEFOLD TACTICS SIGNAL checkpoint='..checkpoint..' clock='..string.format('%.3f',g.sequence_clock)..' lit='..(state.lit and state.order or 0))
   self.tactics_checkpoint=checkpoint+1
  end
 end
end
return F
