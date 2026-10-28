-- Pure gameplay math. Native Defold owns rendering, input, storage and audio.
local M={}
function M.dist(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
function M.norm(a)local n=math.sqrt(a[1]^2+a[2]^2);if n<.000001 then return {1,0}end;return {a[1]/n,a[2]/n}end
function M.segment(p,a,b)local x,y=b[1]-a[1],b[2]-a[2];local t=math.max(0,math.min(1,((p[1]-a[1])*x+(p[2]-a[2])*y)/math.max(.000001,x*x+y*y)));return M.dist(p,{a[1]+x*t,a[2]+y*t})end
function M.ray(o,d,length,walls)
 local best=nil
 for _,w in ipairs(walls)do local r=w.r;local sides={{r[1],1,{-1,0}},{r[1]+r[3],1,{1,0}},{r[2],2,{0,-1}},{r[2]+r[4],2,{0,1}}}
  for _,s in ipairs(sides)do local axis=s[2];local other=3-axis;if math.abs(d[axis])>.000001 then local t=(s[1]-o[axis])/d[axis];local p={o[1]+d[1]*t,o[2]+d[2]*t};if t>.001 and t<length and p[other]>=r[other]-.0001 and p[other]<=r[other]+r[other+2]+.0001 then length=t;best={p=p,n=s[3],type=w.type,t=t}end end end
 end
 return best
end
function M.new(data,saved)
 local g={data=data,saved=saved or {earned={},clues={},weapon='pulse'},paused=true,clock=0,say=function()end,changed=function()end}
 g.saved.earned=g.saved.earned or {};g.saved.clues=g.saved.clues or {}
 function g:total()local n=0;for k,v in pairs(self.saved.earned)do if v then n=n+(data.rewards[k]or 0)end end;return n end
 function g:credits()local n=0;for _,key in ipairs(data.hint_completion_keys)do if self.saved.earned[key]then n=n+2 end end;return n-#self.saved.clues end
 function g:level()local n=0;for _,id in ipairs(self.saved.clues)do if id:sub(1,#self.m.id+1)==self.m.id..':'then n=n+1 end end;return n end
 function g:award(id)if self.saved.earned[id]then return 0 end;local n=data.rewards[id];if not n then return 0 end;local before=self:total();self.saved.earned[id]=true;if before<100 and self:total()>=100 then self.saved.weapon='prism'end;self.changed();return n end
 function g:open()return self.clock%8>=5 end
 function g:active()local walls={};for _,w in ipairs(self.walls)do walls[#walls+1]=w end;if self.m.gate_rect and not self:open()then walls[#walls+1]={r=self.m.gate_rect,type='gate'}end;return walls end
 function g:blocked(p)if p[1]<-6.5 or p[1]>6.5 or p[2]<-4.5 or p[2]>4.5 then return true end;for _,w in ipairs(self:active())do local r=w.r;if p[1]>r[1]-.28 and p[1]<r[1]+r[3]+.28 and p[2]>r[2]-.28 and p[2]<r[2]+r[4]+.28 then return true end end;return false end
 function g:load(index)
  self.index=index;self.m=data.missions[index];self.p={self.m.spawn[1],self.m.spawn[2]};self.aim=M.norm({8.5,-11.9});self.clock=0;self.path={};self.bullets={};self.shots_fired=0;self.enemies={};self.fx={};self.hp=3+(self:total()>=160 and 1 or 0);self.max_hp=self.hp;self.invulnerable=0;self.cooldown=0;self.dash_cooldown=0;self.dash_time=0;self.damage=0;self.solved=false;self.over=false;self.held=false;self.aiming=false;self.clue_time=0;self.hint_debounce=0;self.heal_used=false;self.feedback=0;self.target=nil
  self.walls={{r={-7,-5,14,.3},type='border'},{r={-7,4.7,14,.3},type='border'},{r={-7,-5,.3,10},type='border'},{r={6.7,-5,.3,10},type='border'}}
  for _,r in ipairs(self.m.covers)do self.walls[#self.walls+1]={r=r,type='cover'}end;for _,r in ipairs(self.m.reflectors)do self.walls[#self.walls+1]={r=r,type='reflector'}end
  for _,t in ipairs(self.m.turrets)do self.enemies[#self.enemies+1]={p={t.position[1],t.position[2]},hp=t.hp or 2,max_hp=t.hp or 2,shield=t.shield,boss=t.boss,burst=t.burst or 1,patrol=t.patrol,waypoint=2,speed=t.speed or 1,timer=t.phase+.7,warning=0,direction={-1,0}}end
  for _,t in ipairs(self.m.relays or{})do self.enemies[#self.enemies+1]={p={t.position[1],t.position[2]},hp=1,max_hp=1,shield=true,kind='relay',timer=999,warning=0,direction={0,1}}end
  self.status='Tippen: laufen. Ziehen und loslassen: Feuer.';self.paused=false;self.dialog=nil
 end
 function g:shot()
  local d={self.aim[1],self.aim[2]};local o={self.p[1]+d[1]*.35,self.p[2]+d[2]*.35};local points={o};local length=28;local max=self:total()>=100 and self.saved.weapon=='prism'and 2 or 1
  for b=0,max+1 do local hit=M.ray(o,d,length,self:active());if not hit then points[#points+1]={o[1]+d[1]*length,o[2]+d[2]*length};break end;points[#points+1]=hit.p;length=length-hit.t;if hit.type~='reflector'or b>=max then break end;local dot=d[1]*hit.n[1]+d[2]*hit.n[2];d={d[1]-2*dot*hit.n[1],d[2]-2*dot*hit.n[2]};o={hit.p[1]+d[1]*.003,hit.p[2]+d[2]*.003}end
  return points
 end
 function g:navigate(target)
  local function cell(p)return {math.max(0,math.min(35,math.floor((p[1]+6.8)/.4+.5))),math.max(0,math.min(25,math.floor((p[2]+4.8)/.4+.5)))}end
  local function point(c)return {c[1]*.4-6.8,c[2]*.4-4.8}end
  local function key(c)return c[2]*36+c[1]end
  local start,finish=cell(self.p),cell(target)
  if self:blocked(point(finish))then local best=1e9;for x=0,35 do for y=0,25 do local c={x,y};local p=point(c);local d=M.dist(p,target);if not self:blocked(p)and d<best then best=d;finish=c end end end end
  local q={start};local parents={[key(start)]=false};local found=false;local i=1
  while i<=#q do local c=q[i];if key(c)==key(finish)then found=true;break end
   for dx=-1,1 do for dy=-1,1 do local n={c[1]+dx,c[2]+dy};if not(dx==0 and dy==0)and n[1]>=0 and n[1]<36 and n[2]>=0 and n[2]<26 and parents[key(n)]==nil and not self:blocked(point(n))then
    if not(dx~=0 and dy~=0 and(self:blocked(point({c[1]+dx,c[2]}))or self:blocked(point({c[1],c[2]+dy}))))then parents[key(n)]=c;q[#q+1]=n end
   end end end;i=i+1
  end
  self.path={};if found then local c=finish;while c do table.insert(self.path,1,point(c));c=parents[key(c)]end elseif self.m.staging and target[2]<-1 then self:navigate(self.m.staging)end
 end
 function g:fire()if self.paused or self.over or self.cooldown>0 then return end;self.cooldown=data.combat.fire_cooldown;self.shots_fired=self.shots_fired+1;local points=self:shot();self.bullets[#self.bullets+1]={points=points,p={points[1][1],points[1][2]},segment=1,enemy=false,speed=data.combat.player_bullet_speed};if self.sfx then self.sfx('fire')end end
 function g:dash()if self.paused or self.over or self.dash_cooldown>0 then return end;if #self.path==0 then self:navigate({self.p[1]+self.aim[1]*2,self.p[2]+self.aim[2]*2})end;self.dash_time=data.player.dash_seconds;self.dash_cooldown=data.player.dash_cooldown*(self.saved.earned['secret:dock']and .8 or 1);self.invulnerable=math.max(self.invulnerable,self.dash_time)end
 function g:hit_player()if self.invulnerable>0 or self.over then return end;self.hp=self.hp-1;self.damage=self.damage+1;self.invulnerable=data.combat.hit_invulnerability;self.feedback=.35;if self.sfx then self.sfx('hit')end;if self.hp<=0 then self.over=true;self.paused=true;self.dialog='defeat';self.held=false;self.say('combat_retry')end end
 function g:finish()if self.solved then return end;self.solved=true;self.over=true;self.held=false;self.path={};local n=self:award('mission:'..self.m.id);if self.damage==0 then n=n+self:award('skill:'..self.m.id)end;self.reward=n;self.paused=true;self.dialog='win';self.say('combat_win')end
 function g:locked(t)
  if not t.boss then return false end
  for _,e in ipairs(self.enemies)do if e.kind=='relay'and e.hp>0 then return true end end
  return false
 end
 function g:hit(t,bounces)
  if self:locked(t)then self.status='RELAIS ZUERST';self.say('raid_relays');return end
  if t.shield and bounces==0 then self.status='SCHILD: Nutze die leuchtende Wand.';self.say(t.kind=='relay'and'raid_relays'or'combat_shield');return end;t.hp=t.hp-1;self.fx[#self.fx+1]={p={t.p[1],t.p[2]},life=.45};if self.sfx then self.sfx('hit')end
  if t.hp<=0 then local alive=false;for _,e in ipairs(self.enemies)do alive=alive or e.hp>0 end;if not alive then if not self.m.exit_required then self:finish()else self.status='KANONEN AUS. Erreiche den Energiekern.'end end end
 end
 function g:hint()
  if self.hint_debounce>0 then return end;self.hint_debounce=1.2;local level=self:level();if level<2 then if self:credits()<=0 then self.say('hints_empty');return end;self.saved.clues[#self.saved.clues+1]=self.m.id..':'..(level+1);self.changed()end;self.clue_time=8;self.say(self.m.id=='dock'and'raid_hint'or(self.m.id=='reactor'and'hint_bank'or'hint_guardian'))
 end
 function g:update(dt)
  if self.paused or self.background or self.over then return end;dt=math.min(.05,dt);self.clock=self.clock+dt
  for _,k in ipairs({'invulnerable','cooldown','dash_time','dash_cooldown','clue_time','hint_debounce','feedback'})do self[k]=math.max(0,self[k]-dt)end
  if self.held then self:fire()end
  if #self.path>0 then local t=self.path[1];local speed=self.dash_time>0 and data.player.dash_speed or(data.player.speed+(self:total()>=230 and math.min(.5,(self:total()-220)/210)or 0));local d=M.dist(t,self.p);local step=math.min(d,speed*dt);local n=M.norm({t[1]-self.p[1],t[2]-self.p[2]});local p={self.p[1]+n[1]*step,self.p[2]+n[2]*step};if not self:blocked(p)then self.p=p;self.facing=math.atan2(n[1],n[2])else self.path={}end;if #self.path>0 and M.dist(self.path[1],self.p)<.04 then table.remove(self.path,1)end end
  for _,t in ipairs(self.enemies)do if t.hp>0 and t.kind~='relay' then
   if t.warning>0 then t.warning=t.warning-dt;if t.warning<=0 then
    for j=1,t.burst do local a=(j-(t.burst+1)/2)*.16;local d={t.direction[1]*math.cos(a)-t.direction[2]*math.sin(a),t.direction[1]*math.sin(a)+t.direction[2]*math.cos(a)};local start={t.p[1],t.p[2]};local hit=M.ray(start,d,20,self:active());self.bullets[#self.bullets+1]={points={start,hit and hit.p or{start[1]+d[1]*20,start[2]+d[2]*20}},p={start[1],start[2]},segment=1,enemy=true,speed=data.combat.enemy_bullet_speed}end
    t.timer=data.combat.enemy_interval end
   else
    if t.patrol then local p=t.patrol[t.waypoint];local d=M.dist(t.p,p);if d<t.speed*dt then t.p={p[1],p[2]};t.waypoint=t.waypoint%#t.patrol+1 else local n=M.norm({p[1]-t.p[1],p[2]-t.p[2]});t.p={t.p[1]+n[1]*t.speed*dt,t.p[2]+n[2]*t.speed*dt}end end
    t.timer=t.timer-dt;local cloak=self:total()>=300 and math.min(.35,(self:total()-280)/180)or 0;if t.timer<=0 and M.dist(t.p,self.p)<13*(1-cloak*.5)*((self.saved.earned['secret:guardian']or self.saved.earned['secret:citadel'])and .9 or 1)then t.warning=data.combat.enemy_warning;t.direction=M.norm({self.p[1]-t.p[1],self.p[2]-t.p[2]})end end
  end end
  for i=#self.bullets,1,-1 do local b=self.bullets[i];local distance=b.speed*dt;local removed=false
   while distance>0 and b.segment<#b.points do local t=b.points[b.segment+1];local step=math.min(distance,M.dist(t,b.p));local n=M.norm({t[1]-b.p[1],t[2]-b.p[2]});local q={b.p[1]+n[1]*step,b.p[2]+n[2]*step}
    if b.enemy then if M.segment(self.p,b.p,q)<.36 then self:hit_player();removed=true end else for _,e in ipairs(self.enemies)do if e.hp>0 and M.segment(e.p,b.p,q)<((self.saved.earned['secret:bank']or self.saved.earned['secret:reactor'])and .56 or .48) then self:hit(e,b.segment-1);removed=true;break end end end
    b.p=q;distance=distance-step;if removed then break end;if M.dist(q,t)<.001 then b.segment=b.segment+1 end;if step<.00001 then break end
   end
   if removed or b.segment>=#b.points then table.remove(self.bullets,i)end
  end
  for i=#self.fx,1,-1 do self.fx[i].life=self.fx[i].life-dt;if self.fx[i].life<=0 then table.remove(self.fx,i)end end
  if self.m.heal and not self.heal_used and self.hp<self.max_hp and M.dist(self.p,self.m.heal)<.65 then self.hp=math.min(self.max_hp,self.hp+1);self.heal_used=true;self.status='+1 ENERGIE';if self.sfx then self.sfx('bounce')end end
  local sp=self.m.secret.position;local d=M.dist(self.p,sp);self.secret_visible=not self.saved.earned['secret:'..self.m.id]and d<2 and not M.ray(self.p,M.norm({sp[1]-self.p[1],sp[2]-self.p[2]}),d-.05,self.walls)
  if self.secret_visible and d<.7 then self:award('secret:'..self.m.id);self.say('combat_loot');self.secret_visible=false end
  if self.m.exit_required and self:open() and M.dist(self.p,self.m.goal)<.8 then local alive=false;for _,t in ipairs(self.enemies)do alive=alive or t.hp>0 end;if not alive then self:finish()end end
 end
 g:load(1);return g
end
return M
