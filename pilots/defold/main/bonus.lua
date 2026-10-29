-- Optional in-world challenges. They never lock the mission exit or next mission.
local B={}
local function dist(a,b)return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2)end
local function complete(g,task)
 if task.done then return end
 task.done=true;g.bonus.completed=g.bonus.completed+1
 local amount=g:award(task.key);task.rewarded=true
 g.status=amount>0 and('BONUS GESCHAFFT + '..amount..' STERNE')or'BONUS ERNEUT GESCHAFFT - STERNE SCHON GESPEICHERT'
 for _,e in ipairs(task.targets)do e.hp=0;e.death_age=0;g.fx[#g.fx+1]={kind='bonus',p={e.p[1],e.p[2]},age=0,life=.65}end
 if g.sfx then g.sfx('bounce')end
end
local function target(g,task,p,order)
 local e={p={p[1],p[2]},hp=task.done and 0 or 1,max_hp=1,optional=true,kind='bonus_'..task.kind,bonus_order=order,bonus_task=task,timer=999,warning=0,direction={0,1}}
 task.targets[#task.targets+1]=e;g.enemies[#g.enemies+1]=e;return e
end
function B.load(g)
 g.bonus={tasks={},completed=0,total=0}
 if not g.data.bonuses_enabled or not g.m.bonuses then return end
 for _,id in ipairs({'prism','pattern'})do
  local spec=g.m.bonuses[id];local kind=id=='prism'and'prism'or spec.kind
  local key='bonus:'..id..':'..g.m.id
  local rewarded=g.saved.earned[key]==true
  local task={id=id,kind=kind,key=key,rewarded=rewarded,replay=g.data.optional_replay==true and rewarded,title=kind=='prism'and'ABPRALL-BONUS'or kind=='sequence'and'LICHTER-BONUS'or'GEDULDS-BONUS',reward=g.data.rewards[key],p={spec.p[1],spec.p[2]},done=rewarded and not g.data.optional_replay,targets={},clock=0,progress=0,sequence=spec.sequence}
  g.bonus.tasks[#g.bonus.tasks+1]=task;g.bonus.total=g.bonus.total+1
  if task.done then g.bonus.completed=g.bonus.completed+1 end
  if kind=='sequence'then for i,p in ipairs(spec.nodes)do target(g,task,p,i)end else target(g,task,spec.p,1)end
 end
end
function B.update(g,dt)
 for _,task in ipairs(g.bonus.tasks)do if not task.done then
  task.clock=task.clock+dt
  if task.kind=='wait'then
   task.green=task.clock%5>=3
   task.targets[1].bonus_green=task.green
  elseif task.kind=='sequence'then
   local phase=task.clock%4.6;local slot=math.floor(phase/.9)+1
   for _,e in ipairs(task.targets)do e.bonus_lit=slot<=3 and task.sequence[slot]==e.bonus_order and phase%.9<.6 end
  end
  -- Explain on discovery, once per visit; never endlessly repeat over combat.
  if not task.announced and not g.voice_busy and dist(g.p,task.p)<2.8 then task.announced=true;g.say('bonus_'..task.kind)end
 end end
end
function B.hit(g,e,bounces)
 if not e.optional then return false end
 local task=e.bonus_task
 if not task or task.done then return true end
 if task.kind=='prism'then
  if bounces>0 then complete(g,task)else g.status='GOLDENER BONUS: UEBER EINE WAND TREFFEN';if not task.retry_voice or task.clock-task.retry_voice>4 then task.retry_voice=task.clock;g.say('bonus_prism')end end
 elseif task.kind=='sequence'then
  if task.sequence[task.progress+1]==e.bonus_order then
   task.progress=task.progress+1;e.lit=.6;g.status='BONUSFOLGE '..task.progress..'/3'
   if task.progress==#task.sequence then complete(g,task)end
  else task.progress=0;task.clock=0;g.status='BONUS: LICHTER NOCH EINMAL ANSEHEN';g.say('bonus_sequence')end
 elseif task.kind=='wait'then
  if task.green then complete(g,task)else
   g.status='BONUS: AUF GRUEN WARTEN'
   if not task.retry_voice or task.clock-task.retry_voice>4 then task.retry_voice=task.clock;g.say('bonus_wait')end
   -- Repeated premature fire cannot brute-force the timing bonus. Waiting starts
   -- again without losing health, points or any main-mission progress.
   task.clock=0;task.green=false;e.bonus_green=false
  end
 end
 return true
end
return B
