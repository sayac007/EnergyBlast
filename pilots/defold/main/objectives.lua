-- Three tactical situations: prepare a trap, remember a sequence, escort a drone.
local O={}
O.catalogue={
 {id='magnet',name='MAGNET',duration=6,cooldown=4,radius=.85,color='b994ff',icon='trap_magnet',label='SCHILD AUS · 6 s'},
 {id='frost',name='EIS',duration=9,cooldown=7,radius=1,color='80ecff',icon='trap_frost',label='LAENGER FEST · 9 s'},
 {id='pulse',name='IMPULS',duration=5,cooldown=8,radius=1.15,damage=2,color='ffd477',icon='trap_pulse',label='2 ENERGIEPUNKTE'}
}
function O.trap_spec(id)
 for _,spec in ipairs(O.catalogue)do if spec.id==(id or'magnet')then return spec end end
end
function O.load(g)
 g.traps={};g.trap_cooldown=0;g.trap_ui=nil;g.tactical_pause=false;g.sequence_progress=0;g.sequence_clock=0;g.sequence_wrong=0
 for i,p in ipairs(g.m.sequence_nodes or{})do g.enemies[#g.enemies+1]={p={p[1],p[2]},hp=1,max_hp=1,kind='sequence',order=i,timer=999,warning=0,direction={0,1}}end
 if g.m.escort then local e=g.m.escort;g.drone={p={e.spawn[1],e.spawn[2]},hp=e.hp,waypoint=1,invulnerable=0,arrived=false}else g.drone=nil end
end
function O.sequence_hit(g,t)
 local expected=g.m.sequence[g.sequence_progress+1]
 if t.order~=expected then
  g.sequence_progress=0;g.sequence_clock=0;g.sequence_wrong=.65;g.status='NEUE FOLGE - SCHAU AUF DIE LICHTER';g.say('defold_echo');return
 end
 g.sequence_progress=g.sequence_progress+1;t.lit=.7;g.status='FOLGE '..g.sequence_progress..'/3'
 if g.sequence_progress==#g.m.sequence then
  for _,e in ipairs(g.enemies)do if e.kind=='sequence'then e.hp=0;e.death_age=0;g.fx[#g.fx+1]={kind='explosion',p={e.p[1],e.p[2]},life=.9,age=0}end end
  local alive=false;for _,e in ipairs(g.enemies)do alive=alive or e.hp>0 end;if not alive then g:finish()end
 end
end
function O.trap(g,p,id)
 local spec=O.trap_spec(id);p=p or g.p
 if not spec or g.paused or g.over or g.trap_cooldown>0 or g.m.kind~='trap'or g:blocked(p)then return false end
 if #g.traps>=2 then table.remove(g.traps,1)end
 g.traps[#g.traps+1]={p={p[1],p[2]},life=12,type=spec.id,radius=spec.radius};g.trap_cooldown=spec.cooldown;g.status=spec.name..' BEREIT - LOCKE DEN WAECHTER';return true
end
function O.drone_hit(g)
 if not g.drone or g.drone.invulnerable>0 or g.over then return end
 g.drone.hp=g.drone.hp-1;g.drone.invulnerable=1
 if g.drone.hp<=0 then g.over=true;g.paused=true;g.dialog='defeat';g.held=false;g.status='DROHNE BRAUCHT EINEN NEUEN ANLAUF';g.say('combat_retry')end
end
function O.update(g,dt,dist)
 g.trap_cooldown=math.max(0,g.trap_cooldown-dt);g.sequence_clock=g.sequence_clock+dt;g.sequence_wrong=math.max(0,g.sequence_wrong-dt)
 for i=#g.traps,1,-1 do local trap=g.traps[i];trap.life=trap.life-dt
  local spec=O.trap_spec(trap.type)
  for _,e in ipairs(g.enemies)do if e.hp>0 and e.kind~='relay'and e.kind~='sequence'and dist(e.p,trap.p)<spec.radius then
   e.trapped=math.max(e.trapped or 0,spec.duration);trap.life=0;g.fx[#g.fx+1]={kind='trap_'..spec.id,p={e.p[1],e.p[2]},age=0,life=.8};g.status='SCHILD AUS - JETZT TREFFEN';g.say('defold_trap_trigger')
   for hit=1,(spec.damage or 0)do g:hit(e,0)end
   break
  end end
  if trap.life<=0 then table.remove(g.traps,i)end
 end
 for _,e in ipairs(g.enemies)do e.trapped=math.max(0,(e.trapped or 0)-dt);e.lit=math.max(0,(e.lit or 0)-dt)end
 local e=g.drone
 if e then
  e.invulnerable=math.max(0,e.invulnerable-dt)
  local target=g.m.escort.route[e.waypoint]
  e.moving=target~=nil and dist(g.p,e.p)<3.2
  if e.moving then
   local dx,dz=target[1]-e.p[1],target[2]-e.p[2];local d=math.sqrt(dx*dx+dz*dz);local step=math.min(d,g.m.escort.speed*dt)
   local p=d>0 and{e.p[1]+dx/d*step,e.p[2]+dz/d*step}or target
   if not g:blocked(p)then e.p=p end
   if dist(e.p,target)<.05 then e.waypoint=e.waypoint+1 end
  end
  e.arrived=e.waypoint>#g.m.escort.route
  if e.arrived and dist(g.p,g.m.goal)<1.2 then g:finish()end
 end
end
return O
