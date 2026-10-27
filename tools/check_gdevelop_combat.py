"""Actual GDevelop shooter runtime: touch gestures, moving shots, threats and save."""
from pathlib import Path
import functools,threading,http.server,json,re
from playwright.sync_api import sync_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory='/tmp/energyblast-gdevelop-web'));threading.Thread(target=server.serve_forever,daemon=True).start();checks=0
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader']);page=browser.new_page(viewport={'width':450,'height':800},has_touch=True,is_mobile=True);errors=[];external=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 def route(r):
  if not r.request.url.startswith(('http://127.0.0.1:','data:','blob:')):external.append(r.request.url);r.abort()
  else:r.continue_()
 page.route('**/*',route)
 def check(exp,message):
  global checks
  checks+=1;assert page.evaluate(exp),message
 def execute(body):return page.evaluate('()=>{let g=globalThis.__energyblast;'+body+'}')
 def step(seconds):execute('g.paused=false;for(let i=0;i<'+str(round(seconds/.025))+';i++)g.update(.025);g.paused=true;')
 def screen(p):return page.evaluate('''p=>{let g=globalThis.__energyblast,v=new THREE.Vector3(p[0]*100,-p[1]*100,0).project(g.layer.getRenderer().getThreeCamera()),r=g.canvas.getBoundingClientRect();return [r.left+(v.x+1)*r.width/2,r.top+(1-v.y)*r.height/2];}''',p)
 page.goto(f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('!!globalThis.__energyblast');execute('g.sound=false;')
 page.get_by_role('button',name=re.compile('PRISMA-STATION')).tap();execute('g.sound=false;g.paused=true;')
 check('globalThis.__energyblast.enemies.length===1&&globalThis.__energyblast.hp===3','Live cannon and real player energy')
 check('globalThis.__energyblast.scene.getGame()._disableMetrics===true','Metrics disabled')
 execute("let root=g.models[0].get3DRendererObject();root.updateMatrixWorld(true);let cover=root.getObjectByName('Cover'),p=cover.getWorldPosition(new THREE.Vector3());globalThis.coverWorld=[p.x,p.y,p.z]")
 check('Math.abs(globalThis.coverWorld[0])<5&&Math.abs(globalThis.coverWorld[1]+120)<5','Visible cover aligns with collision coordinates after glTF axis conversion')
 execute('g.paused=false;');page.touchscreen.tap(*screen([-4,2]));execute('g.paused=true;')
 check('globalThis.__energyblast.path.length>0','Single native touch moves without mode selection')
 execute('g.load(0);g.p=[3,2];g.aim=g.norm([1.5,-2]);g.fire();');step(.4)
 check('globalThis.__energyblast.enemies[0].hp===2','Shield blocks direct fire')
 execute('g.load(0);g.p=[4.5,3.2];');step(1)
 check('globalThis.__energyblast.enemies[0].warning>0','Enemy windup visible')
 execute('globalThis.locked=[...g.enemies[0].direction];g.p=[3.5,3.2];');step(.2)
 check('globalThis.__energyblast.enemies[0].direction.every((v,i)=>v===globalThis.locked[i])','Projectile windup locks aim instead of tracking instantly')
 execute('g.p=[4.5,3.2];');step(1.6)
 check('globalThis.__energyblast.damage>0&&globalThis.__energyblast.hp<3','Enemy projectile actually hits')
 execute('globalThis.oldHp=g.hp;g.damagePlayer();')
 check('globalThis.__energyblast.hp===globalThis.oldHp','Hit protection prevents instant draining')
 execute('g.load(0);');step(4)
 check('globalThis.__energyblast.hp===3','Cover intercepts shells')
 check('globalThis.__energyblast.total()===0','Waiting earns nothing')
 execute('g.paused=false;');session=page.context.new_cdp_session(page);start=screen([-3,2]);end=screen([1.392857,-4.35])
 session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':start[0],'y':start[1],'id':0}]})
 session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':end[0],'y':end[1],'id':0}]})
 session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});execute('g.paused=true;')
 check('globalThis.__energyblast.bullets.some(b=>!b.enemy)','Native touch drag/release fires without a mode button');step(1.8)
 check('globalThis.__energyblast.enemies[0].hp===1','Moving bank shot damages cannon')
 execute('g.paused=false;g.fire();');step(1.8)
 check('globalThis.__energyblast.solved&&globalThis.__energyblast.enemies[0].hp===0','Second reflected hit secures sector')
 check('globalThis.__energyblast.total()===100&&globalThis.__energyblast.hints()===2','Single combat payment and earned hints')
 execute('g.finish();');check('globalThis.__energyblast.total()===100','No repeated victory payment')
 page.reload();page.wait_for_function('!!globalThis.__energyblast');check('globalThis.__energyblast.total()===100','Restart preserves combat stars')
 execute('g.sound=false;g.load(1);g.paused=true;g.clock=0;g.navigate(g.m.goal);')
 check('globalThis.__energyblast.enemies.length===2','Second sector contains two active enemies')
 check('globalThis.__energyblast.path.length>0&&globalThis.__energyblast.path.at(-1)[1]>-1.1','Closed gate stages instead of auto-crossing')
 execute('g.load(0);g.navigate([-3,3.2]);g.dash();');check('globalThis.__energyblast.dashTime>0&&globalThis.__energyblast.invulnerable>0','Dash moves with brief protection')
 execute('globalThis.cooldown=g.dashCooldown;g.dash();globalThis.dashUnchanged=g.dashCooldown===globalThis.cooldown;');check('globalThis.dashUnchanged','Dash cooldown bounded')
 execute('g.invulnerable=0;g.hp=1;g.damagePlayer();');check('globalThis.__energyblast.over&&globalThis.__energyblast.total()===100','Defeat keeps earned points')
 page.get_by_role('button',name=re.compile('NEUER ANLAUF')).tap();check('globalThis.__energyblast.hp===3&&!globalThis.__energyblast.over','Visible restart button works')
 execute('g.sound=false;g.paused=true;');page.wait_for_timeout(500);page.screenshot(path='/tmp/energyblast-v2-gdevelop.png')
 execute('g.saved.earned["mission:bank"]=true;g.saved.earned["skill:bank"]=true;g.saved.clues.push("bank:1");g.save();')
 page.reload();page.wait_for_function('!!globalThis.__energyblast')
 check('globalThis.__energyblast.total()===200','Legacy and new combat stars both retained')
 check('globalThis.__energyblast.hints()===3&&globalThis.__energyblast.saved.clues.includes("bank:1")','Legacy paid clues survive migration')
 execute('g.held=true;g.pointer=true;g.setBackground(true);')
 check('!globalThis.__energyblast.held&&!globalThis.__energyblast.pointer','Background cancels held fire and pending touch')
 execute('g.setBackground(false);')
 assert not errors,errors;assert not external,external;checks+=2
 print(json.dumps({'status':'PASS','checks':checks,'page_errors':errors,'external_requests':external,'scope':'Actual GDevelop WebGL runtime, desktop touch emulation; no physical Android benchmark'},indent=2));browser.close()
server.shutdown()
